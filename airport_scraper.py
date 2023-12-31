import requests
from bs4 import BeautifulSoup
import re
import string
import datetime
import pytz

# Custom Flight and Airport class
from Flight import Flight
from Airport import Airport


# https://www.zenrows.com/blog/user-agent-web-scraping#best
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

timezones = {"CST": "America/Chicago",
             "CDT": "CST6CDT",
             "MST": "MST",
             "MDT": "MST7MDT",
             "EST": "EST",
             "EDT": "EST5EDT",
             "PDT": "PST8PDT",
             "AST": "US/Alaska",
             "AKDT": "US/Aleutian",
             "JST": "Japan",
             "HKT": "Asia/Hong_Kong"}

# print(pytz.all_timezones_set)

printable = set(string.printable)

# Get all airports
with open("airports.txt", "r") as airports_file:
    all_airport_codes = airports_file.read().split("\n")


def formatted_time_to_datetime(time, a_or_p):
    # "12:00pCST" to datetime
    today = datetime.date.today()

    split_time = time.split(a_or_p)
    # First element is hour/minute, second element is time zone
    hour = int(split_time[0].split(":")[0])
    if hour == 12:
        hour = 0
    if a_or_p == "p":
        hour = hour + 12
    minute = int(split_time[0].split(":")[1])
    time = datetime.datetime(today.year, today.month, today.day, hour, minute, 0, 0)
    tz_string = split_time[1]
    if tz_string not in pytz.all_timezones_set:
        tz_string = timezones[tz_string]
    #return time.replace(tzinfo=pytz.timezone(tz_string))
    return pytz.timezone(tz_string).localize(time)


def get_airport_flights(airport_code):
    global airportless_url, headers

    airportless_url = "https://www.flightaware.com/live/airport/"
    page = requests.get(airportless_url + airport_code)
    soup = BeautifulSoup(page.text, "html.parser")

    airport_board = soup.find("table", {"class": "fullWidth airportBoard", "data-type": "departures"})

    rows = airport_board.find_all("tr", id=re.compile('^Row_outbound_'))

    flights = []
    for row in rows:
        tds = row.find_all("td")
        info = [''.join(filter(lambda x: x in printable, td.text.strip())) for td in tds if len(td.text.strip()) > 0]

        if len(info) != 5 or "(" not in info[2]:
            # Missing data field. Can't use
            print(f"Can't use {info}: Missing Data Field")
            continue

        # Structure: ID, Plane, Destination Name, Destination Code, Depart, Arrive
        dest_code = info[2].split("(")[1].split(")")[0]
        if len(dest_code) < 4:
            dest_code = "K" + dest_code  # We're just going to assume this
        if dest_code not in all_airport_codes or dest_code == airport_code:
            print(f"No valid destination! ({dest_code})")
            continue
        info.insert(3, dest_code)

        # idx 4 and 5 are times in different timezones
        has_error = False
        for t_idx in (4,5):
            time = info[t_idx]
            if "(?)" in time:
                print("Error: Malformatted time! (?) why is this in here?")
                has_error = True
                break
            if "a" in time:
                info[t_idx] = formatted_time_to_datetime(time, "a")
            elif "p" in time:
                info[t_idx] = formatted_time_to_datetime(time, "p")
            else:
                print("Error: Malformatted time!")
                has_error = True
                break
        if has_error:
            break
        #print(info[4], info[5], info[5] - info[4], (info[5] - info[4]).total_seconds())
        new_info = [info[0], info[1], info[2], info[3], (info[5] - info[4]).total_seconds()]
        if (info[5] - info[4]).total_seconds() < 0:
            print()
        try:
            f = Flight(*new_info)
            flights.append(f)  # unrolling list into args
        except Exception as e:
            # he he he
            print(f"Exception: {e}")

    return flights


def make_planes_histogram():
    global all_airport_codes
    # Get a list of all airports

    counter = 0

    planes_hist = {}
    for airport in all_airport_codes[:10]:
        print(airport)
        flights = get_airport_flights(airport_code=airport)

        for flight in flights:
            # Must check whether airport is in list of airports
            if flight.plane not in planes_hist:
                planes_hist[flight.plane] = 0
            planes_hist[flight.plane] += 1
            counter += 1

    print(planes_hist)
    print(counter)


def get_airport(airport_code):
    # Gets information like name, geographical position, flights and returns an Airport object with it
    codeless_url = "https://www.flightaware.com/resources/airport/"
    page = requests.get(codeless_url + airport_code)
    soup = BeautifulSoup(page.text, "html.parser")

    info_table = soup.find("table", {"class": "prettyTable tablesaw tablesaw-stack"})

    info_rows = info_table.find_all("tr")

    tds = info_rows[1].find_all("td", {"class": "smallrow1"})
    a = tds[0].find("a")
    name = a.text.split(",")[0]

    tds = info_rows[1].find_all("td", {"class": "smallrow2"})

    position_data = tds[0].text
    coords = position_data.strip().split("\n")[0]
    coords = [float(datum) for datum in coords.split(",")]
    elev = float(position_data.strip().split("\n")[1].split("/")[1].replace("meters", ""))

    flights = get_airport_flights(airport_code)

    return Airport(id=airport_code, name=name, coordinates=coords, elev=elev, flights=flights)


