import airport_scraper
from Flight import Flight
from Airport import Airport
import math


class flight_graph:
    def __init__(self):
        self.flightGraph = {}
        with open("airports.txt") as f:
            all_codes = f.read().split("\n")
            for code in all_codes[:10]:
                print("Code: " + code)
                self.flightGraph[code] = airport_scraper.get_airport(code)

    def as_dict(self):
        new_dict = {}
        for key, value in self.flightGraph.items():
            new_dict[key] = value.as_dict()
        return new_dict

    def get_flight(self,start_airport,end_airport,carbon_weight,time_weight,cost_weight):
        unvisited = set({})
        distances = {}
        for code in self.flightGraph:
            distances[code] = math.inf
            unvisited.add(code)
        while len(unvisited) > 0:
            currAirport = min(unvisited)
            

if __name__ == "__main__":
    print(flight_graph().as_dict())