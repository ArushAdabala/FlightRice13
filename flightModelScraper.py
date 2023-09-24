import requests
from bs4 import BeautifulSoup

f = open("airplanemodels.txt","w")
url = "http://fi-aeroweb.com/US-Commercial-Aircraft-Fleet.html"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

airports = soup.find_all("p", {"class" : "style5"})
airports = airports[:2]
airports[0] = str(airports[0]).split("<br/>")[1:]
airports[1] = str(airports[1]).split("<br/>")[1:]
for i in range(len(airports[0])):
    print(str(airports[0][i][1:] + " " + airports[1][i][1:]))

f.close()