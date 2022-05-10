

class DeviceObject:

    def __init__(self, id, accound_holder_id, status):
        self.id = id
        self.accound_holder_id = accound_holder_id
        self.status = status
        self.data = []
        self.track_found = False
        self.current_track = None
        self.current_latitude = None
        self.current_longitude = None

    def __str__(self):
        return "DeviceData: {}, {}, {}, {}, {}".format(self.id, self.name, self.type, self.location, self.status)

    def __repr__(self):
        return self.__str__()


    def addToObject(self, data):
        self.data.append(data)
    
    def setId(self, id):
        self.id = id
    
    def setAccountHolderId(self, accound_holder_id):
        self.accound_holder_id = accound_holder_id
    
    def setStatus(self, status):
        self.status = status
    
    def setTrackFound(self, track_found):
        self.track_found = track_found
    
    def setCurrentTrack(self, current_track):
        self.current_track = current_track
    
    def setCurrentLatitude(self, current_latitude):
        self.current_latitude = current_latitude
    
    def setCurrentLongitude(self, current_longitude):
        self.current_longitude = current_longitude
    



class DeviceData:

    def __init__(self, timestamp, latitude, longitude, altitude, epv, ept, speed, climb):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.epv = epv
        self.ept = ept
        self.speed = speed
        self.climb = climb

    def __str__(self):
        return "DeviceData: {}, {}, {}, {}, {}, {}, {}, {}".format(self.timestamp, self.latitude, self.longitude, self.altitude, self.epv, self.ept, self.speed, self.climb)

    def __repr__(self):
        return self.__str__()
