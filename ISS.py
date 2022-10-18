import time
from urllib import request
import json
from numpy import sin, cos, arccos, pi, round
import datetime

lobez_longitude = 15.6213487
lobez_latitude = 53.6391189

def iss_api_get():
    req_url = request.urlopen("http://api.open-notify.org/iss-now.json")
    # req = requests.get("http://api.open-notify.org/iss-now.json")
    obj = json.loads(req_url.read())
    dt = datetime.datetime.fromtimestamp(obj['timestamp'])
    date_time = str(dt)
    iss_longitude = float(obj['iss_position']['longitude'])
    iss_latitude = float(obj['iss_position']['latitude'])
    return date_time,iss_longitude, iss_latitude




def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians



def distance_lob_iss(iss_latitude, iss_longitude):
    global lobez_longitude, lobez_latitude
    theta = iss_longitude - lobez_longitude

    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(iss_latitude)) * sin(deg2rad(lobez_latitude))) +
            (cos(deg2rad(iss_latitude)) * cos(deg2rad(lobez_latitude)) * cos(deg2rad(theta)))
        )
    )


    return round(distance * 1.609344, 2)


def write_file(dist,date_time, iss_longitude,iss_latitude):
    iss_pos = str([date_time[:-3], iss_longitude, iss_latitude, f'Odleglosc ISS od Lobza to: {dist} km'])

    with open('ISS_pos.txt', 'a+') as f:
        f.write(iss_pos + '\n')

def action():
    date_time,iss_longitude, iss_latitude = iss_api_get()
    dist = distance_lob_iss(iss_latitude,iss_longitude)
    write_file(dist,date_time, iss_longitude,iss_latitude)
    time.sleep(300)


if __name__ == "__main__":
    while True:
        action()

