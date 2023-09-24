class Airport:
    def __init__(self, id, name, coords, elev, flights):
        self.id = id  # string
        self.name = name  # string
        self.coordinates = coords  # 2-tuple
        self.elev = elev  # float
        self.flights = flights  # list of Flights

    def get_size(self):
        return len(self.flights)
    def get_flights(self):
        return self.flights

    def get_coordinates(self):
        return self.coordinates

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def as_dict(self):
        flights_dicts = []
        for flight in self.flights:
            flights_dicts.append(flight.__dict__)
        return Airport(self.id, self.name, self.coordinates, self.elev, flights_dicts).__dict__

    def __str__(self):
        return f"{self.name} airport {self.id} with {len(self.flights)} flights"