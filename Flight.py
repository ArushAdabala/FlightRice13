class Flight:
    def __init__(self, id, plane, dest_name, dest_code, depart_time, arrive_time):
        self.id = id  # string
        self.plane = plane  # string
        self.dest_name = dest_name  # string
        self.dest_code = dest_code  # string, 4 chars
        self.depart_time = depart_time  # datetime
        self.arrive_time = arrive_time  # datetime

    def get_flight_duration(self):
        return self.arrive_time - self.depart_time

    def get_plane_carbon_factor(self):
        # unimplemented
        return

    def get_flight_cost(self):
        #unimplemented
        return

    def __str__(self):
        return f"Flight {self.id} to {self.dest_name} at {self.depart_time.strftime('%H:%M:%S')}"
