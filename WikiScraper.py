import requests
from bs4 import BeautifulSoup

f = open("airports.txt","w")
url = "https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

airports = soup.find("table", {"class" : "wikitable sortable"})
for tr in airports.find_all('tr'):
    a = tr.find_all("td")
    code = a[3].text if len(a) > 3 else ""
    # Take out all airports whose codes don't start with K (continental US)
    if len(code) > 0 and code[0] == "K":
        f.write(code)

f.close()
