import requests
from bs4 import BeautifulSoup
import re
import string
import datetime
import pytz

airportless_url = "https://www.flightaware.com/live/airport/"

# https://www.zenrows.com/blog/user-agent-web-scraping#best
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

timezones = {"CST": "America/Chicago", "CDT": "CST6CDT", "MST": "MST", "MDT": "MST7MDT", "EST": "EST", "EDT": "EST5EDT", "PDT": "PST8PDT"}


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
    return time.replace(tzinfo=pytz.timezone(timezones[split_time[1]]))


def get_airport_flights(airport_code):
    global airportless_url, headers

    page = requests.get(airportless_url + airport_code)
    soup = BeautifulSoup(page.text, "html.parser")

    airport_board = soup.find("table", {"class": "fullWidth airportBoard", "data-type": "departures"})

    rows = airport_board.find_all("tr", id=re.compile('^Row_outbound_'))

    printable = set(string.printable)

    flights = []
    for row in rows:
        tds = row.find_all("td")
        info = [''.join(filter(lambda x: x in printable, td.text.strip())) for td in tds if len(td.text.strip()) > 0]

        if len(info) != 5:
            # Missing data field. Can't use
            break


        # idx 3 and 4 are times in different timezones
        for t_idx in (3,4):
            time = info[t_idx]
            if "a" in time:
                info[t_idx] = formatted_time_to_datetime(time, "a")
            elif "p" in time:
                info[t_idx] = formatted_time_to_datetime(time, "p")
            else:
                print("Error: Malformatted time!")

        flights.append(info)

    return flights


print(get_airport_flights(airport_code="KIAH"))