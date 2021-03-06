class RaceTrack:
    def __init__(self, track_id, track_name, start_latitude, start_longitude, ):
        self.track_id = track_id
        self.track_name = track_name
        self.start_longitude = start_longitude
        self.start_latitude = start_latitude
    
    def __str__(self):
        return "RaceTrack: {}, {}, {}, {}".format(self.track_id, self.track_name, self.start_latitude, self.start_longitude)
    
    def __repr__(self):
        return self.__str__()
    
