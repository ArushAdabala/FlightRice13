class Flight:
    def __init__(self, id, plane, dest_name, dest_code, depart_time, arrive_time):
        planeCarbonOutput = {'P180': 76, 'BE55': 64, 'C208': 67, 'B737': 168, 'P208': 67, 'PA44': 63, 'M7': 78, 'E170': 157, 'C560': 77, 'COL4': 64, 'C320': 69, 'BE58': 61, 'C425': 77, 'B772': 70, 'GLF4': 64, 'J5': 69, 'BL8': 61, 'BE20': 108, 'B38M': 85, 'AT43': 77, 'C441': 72, 'C210': 77, 'C340': 70, 'C180': 61, 'B763': 93, 'EPIC': 63, 'C56X': 72, 'R44': 61, 'P28B': 68, 'A20N': 127, 'PA23': 71, 'C172': 62, 'B58T': 78, 'H269': 75, 'DA62': 75, 'A306': 72, 'C82T': 75, 'LJ60': 74, 'C68A': 78, 'AT8T': 73, 'AC11': 60, 'CH7A': 72, 'PRM1': 78, 'P46T': 66, 'RV12': 66, 'KODI': 74, 'BE23': 77, 'P28R': 78, 'B744': 75, 'C162': 76, 'PA32': 61, 'H25B': 65, 'P32T': 78, 'C310': 64, 'GL5T': 61, 'BCS3': 72, 'B412': 76, 'MD11': 66, 'FA7X': 67, 'DA42': 77, 'UH1': 63, 'CL60': 74, 'E50P': 61, 'AA5': 64, 'GLF6': 60, 'EC45': 60, 'B739': 100, 'P210': 74, 'A119': 64, 'E545': 75, 'BE65': 65, 'EC30': 66, 'PA46': 70, 'PA27': 75, 'C25C': 73, 'PA38': 69, 'CL35': 68, 'PA31': 64, 'P28T': 78, 'B753': 66, 'DV20': 72, 'E300': 60, 'E135': 75, 'H25C': 65, 'C680': 70, 'J328': 66, 'C750': 66, 'SR20': 68, 'PC12': 61, 'C510': 77, 'P32R': 66, 'A319': 153, 'BE30': 71, 'E120': 68, 'MD82': 72, 'BE36': 79, 'PC24': 69, 'B350': 69, 'R22': 78, 'AS50': 69, 'EC35': 64, 'B712': 131, 'G150': 70, 'E45X': 168, 'T206': 69, 'DHC6': 61, 'C82S': 77, 'E190': 149, 'R66': 66, 'S22T': 77, 'C402': 74, 'C185': 71, 'C421': 65, 'T6': 70, 'P212': 70, 'BE35': 76, 'PA24': 62, 'B190': 91, 'BE40': 65, 'BE9L': 69, 'E75L': 179, 'PAY1': 70, 'B06': 69, 'B764': 64, 'C195': 68, 'GALX': 60, 'A321': 103, 'BE18': 64, 'TBM9': 65, 'C25B': 77, 'B752': 107, 'T210': 79, 'PA30': 76, 'H500': 65, 'BL17': 76, 'E145': 139, 'E195': 68, 'BE33': 65, 'SR22': 78, 'C82R': 61, 'PA22': 65, 'GA7C': 74, 'C500': 62, 'TAMP': 63, 'DA40': 72, 'P28A': 66, 'GA5C': 64, 'M20T': 63, 'A139': 76, 'C404': 69, 'B407': 75, 'C650': 74, 'BCS1': 69, 'AT46': 60, 'MD83': 74, 'C150': 78, 'C525': 62, 'LJ45': 60, 'C206': 79, 'C182': 73, 'B733': 78, 'AT72': 68, 'G280': 66, 'EA50': 73, 'BE99': 108, 'TWEN': 67, 'CRJ2': 61, 'E55P': 167, 'B788': 71, 'CL30': 76, 'M20P': 72, 'PA18': 66, 'C152': 70, 'SH36': 79, 'GL7T': 77, 'C550': 62, 'A21N': 155, 'B738': 116, 'LJ35': 68, 'BT36': 65, 'B39M': 62, 'C700': 73, 'SW4': 60, 'B734': 64, 'TBM7': 77, 'CRJ9': 68, 'SF50': 76, 'C337': 60, 'SLG2': 78, 'PA34': 62, 'GLEX': 77, 'A320': 101, 'F900': 79, 'C240': 71, 'F2TH': 62, 'GA6C': 79, 'BE77': 76, 'CRJ7': 70, 'M600': 74, 'FA10': 64, 'HDJT': 71, 'SB20': 64, 'C25A': 61, 'C188': 79}
        self.id = id  # string
        self.plane = plane  # string
        self.dest_name = dest_name  # string
        self.dest_code = dest_code  # string, 4 chars
        self.depart_time = depart_time  # datetime
        self.arrive_time = arrive_time  # datetime
        self.carbon = planeCarbonOutput[plane] if plane in planeCarbonOutput else 69

    def get_arrival_time(self):
        return self.arrive_time
    def get_departure_time(self):
        return self.depart_time
    def get_flight_duration(self):
        return self.arrive_time - self.depart_time

    def get_plane_carbon_factor(self):
        # unimplemented
        return self.carbon

    def get_plane_carbon_factor(self):
        # unimplemented
        return self.carbon

    def __str__(self):
        return f"Flight {self.id} to {self.dest_name} at {self.depart_time.strftime('%H:%M:%S')}"
