from __future__ import print_function
from gettext import find
import math
from multiprocessing import Process
from sqlite3 import Timestamp
# from threading import Thread, currentThread
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource, reqparse
import logging
from flask import Flask, jsonify, request
# from multiprocessing import Process, Value
from flaskext.mysql import MySQL
from itsdangerous import json
import pymysql
import sys
from pathlib import Path
import uuid
from settings import *
from gps import *
import time
from Device import DeviceObject, DeviceData
from RaceTrack import RaceTrack
from utils import *
import logging
import sys
from math import radians, cos, sin, asin, sqrt

logformat = "%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s"
datefmt = "%m-%d %H:%M"

logging.basicConfig(filename="app.log", level=logging.INFO, filemode="w",
                    format=logformat, datefmt=datefmt)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(logging.Formatter(fmt=logformat, datefmt=datefmt))

logger = logging.getLogger("app")
logger.addHandler(stream_handler)

connectedToDB = False
# main db connection
try:
    db = pymysql.connect(**mainConfig)
    connectedToDB = True
except:

    pass

# device config api
deviceID = 0
# device_id, accound_holder_id, device_data, device_status
CurrentDevice = DeviceObject(deviceID, "", "")
CurrentRaceTrack = None

app = Flask(__name__)
CORS(app)
api = Api(
    app,
    version=API_VERSION,
    title="Flask backend api",
    description="The backend api system for the Electron Vue app",
    doc="/docs",
)

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)


@api.route("/api_version", endpoint="apiVersion")
class ApiVersion(Resource):
    global logger

    def get(self):
        logger.info(f'{API_VERSION} is the current version!')
        return API_VERSION


@api.route("/echo", endpoint="echo")
class HelloWorld(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        global deviceID, logger, connectedToDB, deviceUrl
        if request.method == 'GET':
            try:
                # this is for the first time load only to create the file
                # check if the device config file exists if not create it and write the device id to it
                if not Path(deviceUrl).is_file():
                    with open(deviceUrl, "w") as f:
                        deviceID = str(uuid.uuid4())
                        f.write(deviceID)
                        f.close()

                        # insert device id into the device table
                        cursor = db.cursor()
                        sql = "INSERT INTO `enable_ninja_local`.device_x_user (device_id) VALUES (%s)"
                        val = (deviceID)
                        cursor.execute(sql, val)
                        db.commit()
                else:
                    # read the device id from the file
                    with open(deviceUrl, "r") as f:
                        deviceID = f.read()
                        f.close()

                # query to check to see if the device id has an account associated with it
                if connectedToDB is not False:
                    cursor = db.cursor()
                    sql = "SELECT * FROM `enable_ninja_local`.device_x_user WHERE DEVICE_ID = %s"
                    val = (deviceID)

                    cursor.execute(sql, val)
                response = "Server active!!"
                CurrentDevice.setId(deviceID)
                # CurrentDevice.setAccountHolderId(cursor.fetchone()[1])
                CurrentDevice.setStatus('active')
                return response
            except Exception as e:
                logger.error(
                    {"error": f"An error occurred in the echo method with exception ({e})"})
                return jsonify({"error": f"An error occurred in the index method with exception ({e})"})


# Request parser documentation can be found here: https://flask-restx.readthedocs.io/en/latest/parsing.html
timer = api.namespace("timer", description="timer operations")


@app.route('/add', methods=['POST'])
def add_session():
    """
    This method is used to add a new session to the database
    :return:
        either a json object with the session id or an error message
    """
    global logger, CurrentDevice, connectedToDB
    if request.method == 'POST':
        try:
            results = []
            form = request.get_json(silent=True).get('form')
            if connectedToDB is not False:
                cursor = db.cursor()
            for i in form:
                try:
                    # insert data in database
                    if connectedToDB is not False:
                        cursor.execute(
                            "INSERT INTO `enable_ninja_local`.track_session (created_date, average_lap, fastest_lap, device_id) VALUES (%s, %s, %s, %s)",
                            (i['sessionDate'], i['avgLap'], i['fastestLap'], deviceID))
                        db.commit()

                        # get last inserted id
                        cursor.execute(
                            "SELECT SESSION_ID FROM `enable_ninja_local`.track_session ORDER BY SESSION_ID DESC LIMIT 1")
                        seshID = cursor.fetchone()[0]
                        print(seshID)
                except:
                    pass
                with open("session_data.txt", "a") as file1:
                    # Writing data to a file
                    file1.write(f" {i['sessionDate']}, {i['avgLap']}, {i['fastestLap']} + '\n'")

                # insert data in lap table
                for j in i['laps']:
                    try:
                        if connectedToDB is not False:
                            cursor.execute(
                                "INSERT INTO `enable_ninja_local`.lap (track_session_id, lap_number, lap_time, lap_time_diff) VALUES (%s, %s, %s, %s)",
                                (int(seshID), j['lap'], j['time'], j['timeDiff']))
                            db.commit()
                    except:
                        pass
                    with open("session_data.txt", "a") as file1:
                        # Writing data to a file
                        file1.write(f"{int(seshID)}, {j['lap']}, {j['time']}, {j['timeDiff']} + '\n'")

            with open("session_data.txt", "a") as file1:
                # Writing data to a file
                file1.write("End Entry \n")
            return jsonify("success")
        except Exception as e:
            logger.error(
                {"error": f"An error occurred in the add_session method with exception ({e})"})
            return jsonify({"error": ("An error occurred in the add_session method with exception (%s)", e)})


@api.route("/start", endpoint="start")
class Start(Resource):
    global logger

    def get(self):
        global CurrentDevice, CurrentRaceTrack
        try:
            recording_on = True
            if CurrentDevice.status == "active":
                raceTrackMethod = findClosestTrack(CurrentDevice)
                # logger.error({"error": f"An error occurred in the start method with exception ({raceTrackMethod})"})
                if raceTrackMethod != None:
                    CurrentRaceTrack = raceTrackMethod
                    CurrentDevice.setTrackFound(True)
                    CurrentDevice.setCurrentTrack(CurrentRaceTrack)

            # p = Process(target=Start_Recording_Data, args=(recording_on,))
            # p.start()
            if CurrentRaceTrack != None:
                return jsonify({"track": CurrentRaceTrack.track_name, "lat": CurrentRaceTrack.start_latitude,
                                "lon": CurrentRaceTrack.start_longitude})
            else:
                return jsonify({"error": "No track found"})
        except Exception as e:
            logger.error({"error": f"An error occurred in the start method with exception ({e})"})
            return jsonify({"error": f"An error occurred in the start method with exception ({e})"})


@api.route("/GetIfLapped", endpoint="getIfLapped")
class GetIfLapped(Resource):
    global logger

    def get(self):
        global CurrentDevice, CurrentRaceTrack, gpsd
        try:
            if CurrentDevice is not None and CurrentRaceTrack is not None:
                report = gpsd.next()
                obj = parseGPSData(report)
                logger.info(f"im recording data---{obj}")
                CurrentDevice.addToObject(obj)
                CurrentDevice.current_latitude = obj.latitude
                CurrentDevice.current_longitude = obj.longitude

                # CurrentDevice.current_latitude = 38.5785788
                # CurrentDevice.current_longitude = -77.3046977
                print(type(obj.latitude))
                if obj.latitude is not float(0.0):
                    with open("session_data.txt", "a") as file1:
                        # Writing data to a file
                        file1.write(obj.printObject() + "\n")
                Px = float(CurrentDevice.current_latitude)
                Py = float(CurrentDevice.current_longitude)

                logger.info(
                    {"testing": f"Value ({CurrentRaceTrack})"})
                Qx = float(CurrentRaceTrack.start_latitude)
                Qy = float(CurrentRaceTrack.start_longitude)

                # distVal = math.dist([Px, Py], [Qx, Qy])
                lapped = lappedHelper(Py, Px, Qy, Qx)
                if lapped[0]:
                    # return jsonify({'it works'})
                    logger.info({
                        "inlapped true retrun": "trrue",
                        "lapped": "true",
                        'currentRaceTrack': CurrentRaceTrack.track_name,
                        "lat": CurrentRaceTrack.start_latitude,
                        "lon": CurrentRaceTrack.start_longitude,
                        "helper": lapped[1]}
                    )
                    return jsonify(
                        {
                            "lapped": "true",
                            'currentRaceTrack': CurrentRaceTrack.track_name,
                            "lat": CurrentRaceTrack.start_latitude,
                            "lon": CurrentRaceTrack.start_longitude,
                            "helper": lapped[1]
                        })
                logger.info({
                    "inlapped false retrun": "false",
                    "lapped": "false",
                    "race_track_lat": CurrentRaceTrack.start_latitude,
                    "race_track_lon": CurrentRaceTrack.start_longitude,
                    'device_lat': Px,
                    'device_lon': Py,
                    "helper": lapped[1]}
                )
                return jsonify(
                    {
                        "lapped": "false",
                        "race_track_lat": CurrentRaceTrack.start_latitude,
                        "race_track_lon": CurrentRaceTrack.start_longitude,
                        'device_lat': Px,
                        'device_lon': Py,
                        "helper": lapped[1]
                    })
                # return jsonify({'it doesnt work'})
            else:
                return jsonify({"message": "Either the Device or the race track was not found"})
        except Exception as e:
            logger.error(
                {"error": f"An error occurred in the GetIfLapped method with exception ({e})"})
            return jsonify({"error": f"An error occurred in the getIfLapped method with exception ({e})"})


def Start_Recording_Data(append_to_object):
    global logger, gpsd
    try:
        global CurrentDevice, CurrentRaceTrack
        while True:
            report = gpsd.next()
            obj = parseGPSData(report)
            logger.info(f"im recording data---{obj}")
            if append_to_object == True:
                CurrentDevice.addToObject(obj)
                CurrentDevice.current_latitude = obj.latitude
                CurrentDevice.current_longitude = obj.longitude
            time.sleep(1)
    except Exception as e:
        logger.error(e)
        print(e)


def findClosestTrack(device):
    # Find the closest track to the device
    # Get the tracks from the database
    global logger, CurrentDevice, CurrentRaceTrack, gpsd, connectedToDB
    try:
        report = gpsd.next()
        obj = parseGPSData(report)
        CurrentDevice.current_latitude = obj.latitude
        CurrentDevice.current_longitude = obj.longitude

        # CurrentDevice.current_latitude = 38.5785788
        # CurrentDevice.current_longitude = -77.3046977

        track_list = []
        tracks = []
        if connectedToDB is not False:
            cursor = db.cursor()
            sql = "SELECT * FROM enable_ninja_local.tracks"
            cursor.execute(sql)
            tracks = cursor.fetchall()
        else:
            with open("tracks.txt", 'r') as trackFile:
                tracks = [x.strip() for x in trackFile.readlines()]
        # loop through the tracks and make a list of the track objects

        for i in tracks:
            track_list.append(RaceTrack(i[0], i[1], i[2], i[3]))

        # find the closest track
        allCloseTracks = []
        for i in track_list:
            	print(i)
		if i.start_latitude is not '':
			calc = math.dist([CurrentDevice.current_latitude, CurrentDevice.current_longitude],
                             [float(i.start_latitude), float(i.start_longitude)])
			allCloseTracks.append({'track': i, 'distance': calc})
        if len(allCloseTracks) == 0:
            logger.info(
                {"returnValue": f"None"})
            return None
        else:
            sorted(allCloseTracks, key=lambda d: d['distance'])
            return allCloseTracks[-1]['track']
    except Exception as e:
        logger.error(
            {"error": f"An error occurred in the findClosestTrack method with exception ({e})"})


# 5000 is the flask default port. You can change it to something else if you want.
# Remove `debug=True` when creating the standalone pyinstaller file
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
