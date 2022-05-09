from RaceTrack import RaceTrack
from Device import *
def findClosestTrack(device, db_connection):
    # Find the closest track to the device
    # Get the tracks from the database
    cursor = db_connection.cursor()
    sql = "SELECT * FROM `enable_ninja_local`.tracks"
    cursor.execute(sql)
    tracks = cursor.fetchall()

    # loop through the tracks and make a list of the track objects
    track_list = []
    for i in tracks:
        track_list.append(RaceTrack(i[0], i[1], i[2], i[3]))
    
    # find the closest track
    for i in track_list:
        if math.dist(device.current_latitude, device.current_longitude, i.start_latitude, i.start_longitude) < 20:
            return i
    return None


def parseGPSData(report):
    ret = DeviceData(
        getattr(report,'time',''), 
        getattr(report,'lat',0.0), 
        getattr(report,'lon',0.0), 
        getattr(report,'alt','nan'),
        getattr(report,'epv',"nan"),
        getattr(report,'ept',"nan"),
        getattr(report,'speed',"nan"),
        getattr(report,'climb',"nan"),
    )
    return ret
