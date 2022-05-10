from RaceTrack import RaceTrack
from Device import *
import logging
import math 
import pymysql
from settings import *

logger = logging.getLogger()
handler = logging.FileHandler('logfile.log')
logger.addHandler(handler)




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
