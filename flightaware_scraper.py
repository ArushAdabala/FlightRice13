import requests
from bs4 import BeautifulSoup

url = "https://www.flightaware.com/live/airport/KIAH"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

airport_board = soup.find("table", {"class" : "fullWidth airportBoard"})
# print(airport_board)
row = airport_board.find("tr", {"class": "smallrow1"})
a = row.find_all("a")

print([thing.text for thing in a])

"""
Scrapes airplane data from flightaware
writes data to database of some kind (mySQL? TXT?)
(Approach 1: everything is JS and users update database. Approach 2: database updates done with python on server)
Constructs graph from database

Ui with map and triangle for $/C/T... user inputs
Run's algorithm to determine best route given params
Get result, show user somehow


Possible extensions:
Trains and Boats and stuff
Beautify
"""