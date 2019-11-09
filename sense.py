from sense_hat import SenseHat
import json
import time
import requests
import os
import sqlite3
from sqlite3 import Error

sense = SenseHat()

db = 'webapp/sensor.db'


def sleep(x):
    return time.sleep(x / 1000.0)

# connect to database
def create_connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except Error as e:
        print(e)

    return con


# get settings from database
def get_settings():
    con = create_connection(db)
    cur = con.cursor()
    cur.execute('SELECT * FROM settings')
    results = cur.fetchone()
    settings = None
    if results is not None:
        settings = {
            'userid': results[0],
            'low_temp': results[1],
            'high_temp': results[2],
            'low_humidity': results[3],
            'high_humidity': results[4],
            'low_pressure': results[5],
            'high_pressure': results[6],
            'polling_frequency': results[7]
        }
    return settings


def safe():
    sense.show_message("OK", text_colour=[
                       255, 255, 255], back_colour=[0, 255, 0])


def unsafe():
    os.system('omxplayer warning.mp3')
    sense.show_message("UNSAFE", text_colour=[
                       255, 255, 255], back_colour=[255, 0, 0])


def main():
    settings = get_settings()
    print("Settings: ", settings)

    while True:

        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()

        data = {
            "timestamp": time.time(),
            "temp": round(temp),
            "humidity": round(humidity),
            "pressure": round(pressure)
        }

        # if sensor thresholds are set, check if exceeded
        if settings is not None:
            if(temp > settings['high_temp'] or temp < settings['low_temp']):
                unsafe()
            else:
                safe()

        print(data)

        sleep(2000)


if __name__ == '__main__':
    main()
