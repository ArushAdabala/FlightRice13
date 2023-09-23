import requests
from bs4 import BeautifulSoup

#f = open("airports.txt","w")
url = "https://en.wikipedia.org/wiki/List_of_aircraft_type_designators#:~:text=An%20aircraft%20type%20designator%20is%20a%20two-%2C%20three-,%28ICAO%29%20and%20the%20International%20Air%20Transport%20Association%20%28IATA%29."

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

page = requests.get(url)
soup = soup = BeautifulSoup(page.text, "html.parser")

airports = soup.find("table", {"class" : "wikitable sortable"})

modelsDict = {}
for tr in airports.find_all('tr'):
    a = tr.find_all("td")
    if len(a) > 0:
        newPage = requests.get("https://en.wikipedia.org" + a[2].a.get("href"))
        newSoup = soup = BeautifulSoup(newPage.text, "html.parser")
        info = soup.find("table", {"class": "infobox"})
        flightType = info.find_all('tr')[0]
        print(flightType)


#f.close()
