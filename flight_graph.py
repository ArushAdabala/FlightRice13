import airport_scraper
from Flight import Flight
from Airport import Airport
import math


class flight_graph:
    def __init__(self):
        self.flightGraph = {}
        with open("airports.txt") as f:
            all_codes = f.read().split("\n")
            for code in all_codes:
                self.flightGraph[code] = airport_scraper.get_airport(code)

    def as_dict(self):
        new_dict = {}
        for key, value in self.flightGraph.items():
            new_dict[key] = value.as_dict()
        return new_dict

    def get_flight(self, start_airport, end_airport, carbon_weight, time_weight):
        unvisited = set({})
        distances = {}
        paths = {}

        for code in self.flightGraph:
            distances[code] = math.inf
            paths[code] = [start_airport]
            unvisited.add(code)

        distances[start_airport] = 0

        while len(unvisited) > 0:
            def myfunc(node):
                return distances[node]

            currAirport = min(unvisited, key=myfunc)
            unvisited.remove(currAirport)

            for flight in self.flightGraph[currAirport].get_flights():
                def calc_weights(curr_flight):
                    return curr_flight.get_plane_carbon_factor() * carbon_weight + curr_flight.get_flight_duration() * time_weight
                if distances[currAirport] + calc_weights(flight) < distances[flight.dest_code]:
                    distances[flight.dest_code] = distances[currAirport] + calc_weights(flight)
                    paths[flight.dest_code] = distances[currAirport]

                if distances[flight.dest_code] == end_airport:
                    return (distances[flight.dest_code], paths[flight.dest_code])

        return ("no flight path found")

            

if __name__ == "__main__":
    print(flight_graph().get_flight("KIAH","KATL",0.5,0.5))