from __future__ import print_function
import math
from sqlite3 import Timestamp
from threading import currentThread
from flask import Flask
from calc import calc
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource, reqparse
from datetime import time
import logging
from flask import Flask, jsonify, request
import time
from multiprocessing import Process, Value
from flaskext.mysql import MySQL
import pymysql
import logging
import sys
from pathlib import Path
import uuid
from settings import *
import serial
import pynmea2
from Device import DeviceObject, DeviceData
from RaceTrack import RaceTrack
from utils import *

# main db connection
db = pymysql.connect(**mainConfig)


# device config api
deviceID = 0
# device_id, accound_holder_id, device_data, device_status
CurrentDevice = DeviceObject(deviceID, "", "", "")
CurrentRaceTrack = RaceTrack()

app = Flask(__name__)
CORS(app)
api = Api(
    app,
    version=API_VERSION,
    title="Flask backend api",
    description="The backend api system for the Electron Vue app",
    doc="/docs",
)

serialPort = serial.Serial(port, baudrate=9600, timeout=0.5)


@api.route("/api_version", endpoint="apiVersion")
class ApiVersion(Resource):
    def get(self):
        
        return API_VERSION


@api.route("/echo", endpoint="echo")
class HelloWorld(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        global deviceID
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
                cursor = db.cursor()
                sql = "SELECT * FROM `enable_ninja_local`.device_x_user WHERE DEVICE_ID = %s"
                val = (deviceID)

                cursor.execute(sql, val)
                response = "Server active!!"
                CurrentDevice.device_id = deviceID
                CurrentDevice.accound_holder_id = cursor.fetchone()[1]
                CurrentDevice.device_status = "active"
                return response
            except Exception as e:
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
    if request.method == 'POST':
        try:
            results = []
            form = request.get_json(silent=True).get('form')
            cursor = db.cursor()
            for i in form:
                # insert data in database
                cursor.execute(
                    "INSERT INTO `enable_ninja_local`.track_session (created_date, average_lap, fastest_lap, device_id) VALUES (%s, %s, %s, %s)",
                    (i['sessionDate'], i['avgLap'], i['fastestLap'], deviceID))
                db.commit()

                # get last inserted id
                cursor.execute(
                    "SELECT SESSION_ID FROM `enable_ninja_local`.track_session ORDER BY SESSION_ID DESC LIMIT 1")
                seshID = cursor.fetchone()[0]
                print(seshID)

                # insert data in lap table
                for j in i['laps']:
                    cursor.execute(
                        "INSERT INTO `enable_ninja_local`.lap (track_session_id, lap_number, lap_time, lap_time_diff) VALUES (%s, %s, %s, %s)",
                        (int(seshID), j['lap'], j['time'], j['timeDiff']))
                    db.commit()
            results = cursor.fetchall()
            return jsonify(results)
        except Exception as e:
            print(e)
            return jsonify({"error": ("An error occurred in the add_session method with exception (%s)", e)})


@api.route("/start", endpoint="start")
class Start(Resource):
    def get(self):
        recording_on = Value('b', True)
        p = Process(target=Start_Recording_Data, args=(recording_on))
        p.start()
        return "Recording started"

@api.route("/getIfLapped", endpoint="getIfLapped")
class GetIfLapped(Resource):
    def get(self):
        global CurrentDevice
        Px = CurrentDevice.current_latitude
        Py = CurrentDevice.current_longitude

        Qx = CurrentRaceTrack.start_latitude
        Qy = CurrentRaceTrack.start_longitude

        if math.dist(Px, Py, Qx, Qy) < 5:
            return 1
        return 0

def Start_Recording_Data(append_to_object):
    global finaList, CurrentDevice, serialPort, CurrentRaceTrack
    serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    while True:
        str = serialPort.readline()
        obj = parseGPS(str)
        if CurrentDevice.device_status == "active" and CurrentDevice.track_found == False:
            raceTrackMethod = findClosestTrack(obj, db)

            if raceTrackMethod == "found":
                CurrentRaceTrack = raceTrackMethod[1]
                CurrentDevice.track_found = True
                print("Track found")
        if append_to_object.value == True:
            CurrentDevice.addToObject(obj)
            CurrentDevice.current_latitude = obj.latitude
            CurrentDevice.current_longitude = obj.longitude
        time.sleep(.5)

def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        return DeviceData(timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.num_sats)


# 5000 is the flask default port. You can change it to something else if you want.
# Remove `debug=True` when creating the standalone pyinstaller file
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
