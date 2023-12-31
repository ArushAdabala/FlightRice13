import airport_scraper
from Flight import Flight
from Airport import Airport
import math
import json


class flight_graph:
    def __init__(self, flightGraph=None):
        if flightGraph is None:
            self.flightGraph = {}
            with open("airports.txt") as f:
                all_codes = f.read().split("\n")
                for code in all_codes:
                    self.flightGraph[code] = airport_scraper.get_airport(code)
        else:
            self.flightGraph = flightGraph

    def as_dict(self):
        new_dict = {}
        for key, value in self.flightGraph.items():
            new_dict[key] = value.as_dict()
        return new_dict

    @staticmethod
    def from_dict(graph_dict):
        for key, value in graph_dict.items():
            graph_dict[key] = Airport.from_dict(value)
        return flight_graph(flightGraph=graph_dict)

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
            if currAirport == end_airport:
                return (distances[currAirport], paths[currAirport])
            unvisited.remove(currAirport)

            for flight in self.flightGraph[currAirport].get_flights():
                def calc_weights(curr_flight):
                    return curr_flight.get_plane_carbon_factor() * carbon_weight + curr_flight.get_flight_duration() * time_weight
                if distances[currAirport] + calc_weights(flight) < distances[flight.dest_code]:
                    distances[flight.dest_code] = distances[currAirport] + calc_weights(flight)
                    paths[flight.dest_code] = paths[currAirport] + [flight.dest_code]

        return ("no flight path found")

            

if __name__ == "__main__":

    # Scrape for flight data and save to JSON
    with open("new_graph.json", "w") as json_file:
        fg = flight_graph()
        print([a.flights for a in fg.flightGraph.values()])
        print([[f for f in a.flights] for a in fg.flightGraph.values()])
        json_string = json.dumps(fg.as_dict(), indent=2, sort_keys=True)
        json_file.write(json_string)

    # Load flight data from JSON, skip scraping
    # fg = None
    # with open("graph.json", "r") as json_file:
    #     json_from_file = json.load(json_file)
    #     fg = flight_graph.from_dict(json_from_file)
    #     for a_code, a_val in fg.flightGraph.items():
    #         new_flights = []
    #         for f in a_val.flights:
    #             if f.duration > 0:
    #                 new_flights.append(f)
    #         fg.flightGraph[a_code].flights = new_flights
    # with open("new_graph.json", "w") as json_file:
    #     json_string = json.dumps(fg.as_dict(), indent=2, sort_keys=True)
    #     json_file.write(json_string)


    # with open("graph.json", "r") as json_file:
    #     json_from_file = json.load(json_file)
    #     fg = flight_graph.from_dict(json_from_file)
    #     print(sum([len(a.flights) for a in fg.flightGraph.values()]))
    #     print(fg.get_flight("KATL", "KDFW", 0.5, 0.5))