class Flight:
    def __init__(self, id, plane, dest_name, dest_code, depart_time, arrive_time):
        self.id = id
        self.plane = plane
        self.dest_name = dest_name
        self.dest_code = dest_code
        self.depart_time = depart_time
        self.arrive_time = arrive_time

    def get_flight_duration(self):
        return self.arrive_time - self.depart_time

    def get_plane_carbon_factor(self):
        # unimplemented
        return
