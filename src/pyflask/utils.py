from RaceTrack import RaceTrack
from Device import *
import logging
import math 
import pymysql
from settings import *
from math import radians, cos, sin, asin, sqrt

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

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def lappedHelper(lon1, lat1, lon2, lat2):
    radius = 0.0804672 # in kilometer
    a = haversine(lon1, lat1, lon2, lat2)
    if a <= radius:
        return (True, a)
    else:
        return (False, a)