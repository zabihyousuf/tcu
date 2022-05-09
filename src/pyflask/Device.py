

class DeviceObject:

    def __init__(self, device_id, accound_holder_id, device_status):
        self.device_id = device_id
        self.accound_holder_id = accound_holder_id
        self.device_status = device_status
        self.device_data = []
        self.track_found = False
        self.current_track = None
        self.current_latitude = None
        self.current_longitude = None

    def __str__(self):
        return "DeviceData: {}, {}, {}, {}, {}".format(self.device_id, self.device_name, self.device_type, self.device_location, self.device_status)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.device_id == other.device_id

    def __ne__(self, other):
        return self.device_id != other.device_id

    def addToObject(self, device_data):
        self.device_data.append(device_data)


class DeviceData:

    def __init__(self, device_timestamp, device_latitude, device_latitude_dir, device_longitude, device_longitude_dir, device_altitude, altitude_units, num_sats, device_gyroscope,device_heading):
        self.device_longitude = device_longitude
        self.device_latitude = device_latitude
        # self.device_speed = device_speed
        # self.device_acceleration = device_acceleration
        # self.device_heading = device_heading
        self.device_altitude = device_altitude
        # self.device_gyroscope = device_gyroscope
        self.device_timestamp = device_timestamp
        self.device_latitude_dir = device_latitude_dir
        self.device_longitude_dir = device_longitude_dir
        self.altitude_units = altitude_units
        self.num_sats = num_sats

    def __str__(self):
        return "DeviceData: {}, {}, {}, {}, {}, {}, {}, {}".format(self.device_complete_data, self.device_longitude, self.device_latitude, self.device_speed, self.device_acceleration, self.device_heading, self.device_altitude, self.device_gyroscope)

    def __repr__(self):
        return self.__str__()
