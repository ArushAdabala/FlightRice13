import airport_scraper
from Flight import Flight
from Airport import Airport

class flight_graph:
    def __init__(self):
        f = open("airports.txt")
        self.flightGraph = {}
        for code in f.readline():
            this.flightGraph[code] = airport_scraper.get_airport(code)
        f.close()

    def get_flight(self,start_airport,end_airport,carbon_weight,time_weight,cost_weight):
        unvisited = set({})
        distances = {}
        for code in self.flightGraph:
            distances[code] = math.inf
            unvisited.add(code)
        while len(unvisited) > 0:
            currAirport = min(unvisited)
            



