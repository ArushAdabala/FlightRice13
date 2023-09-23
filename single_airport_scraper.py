import requests
from bs4 import BeautifulSoup
import re
import string

airport_code = "KIAH"

airportless_url = "https://www.flightaware.com/live/airport/"

# https://www.zenrows.com/blog/user-agent-web-scraping#best
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

page = requests.get(airportless_url + airport_code)
soup = BeautifulSoup(page.text, "html.parser")

airport_board = soup.find("table", {"class": "fullWidth airportBoard", "data-type": "departures"})

rows = airport_board.find_all("tr", id=re.compile('^Row_outbound_'))

printable = set(string.printable)

for row in rows:
    tds = row.find_all("td")
    info = [''.join(filter(lambda x: x in printable, td.text.strip())) for td in tds if len(td.text.strip()) > 0]
    print(info)
    #print(info[0])
    #info[0][4].replace(r"\xa0", "[][][]")
    #print(info[0])

print("Done")