class Airport:
    def __init__(self, id, name, coords, elev, flights):
        self.id = id
        self.name = name
        self.coordinates = coords
        self.elev = elev
        self.flights = flights

    def get_size(self):
        return len(self.flights)

    def __str__(self):
        return f"{self.name} airport {self.id} with {len(self.flights)} flights"