

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

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def addToObject(self, data):
        self.data.append(data)


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
