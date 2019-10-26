from database import init_db
from database import db
from flask import Flask, request, send_file, abort
import json
from models import Bow
import os
import math
import csv

SeaLevelPressure = 900

def pressure_to_height(pressure):
    height = ((pressure/SeaLevelPressure)**(1/5.275)-1)*(15+273.15)/0.0065
    return height

def height_to_angle(height1, height2):
    angle = math.asin(height1-height2)
    return angle

def normalize(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        angle_list = []
        normalized_list = []
        for raw in reader:
#            angle_list.append(height_to_angle(pressure_to_height(float(raw[1])), pressure_to_height(float(raw[2]))))
            angle_list.append(height_to_angle(float(raw[1])) - pressure_to_height(float(raw[2])))
        max_length = max(angle_list)
        for angle in angle_list:
            angle = height_to_angle(angle/max_length)
        max_angle = max(angle_list)
        min_angle = min(angle_list)
        for index, angle in enumerate(angle_list):
            normalized_list.append([reader[index][0], str((angle-min_angle)/(max_angle-min_angle))])
        print(normalized_list)
    return normalized_list

app = Flask(__name__)
app.config.from_object('config.Development')
init_db(app)

@app.route("/")
def index():
    return "Hello"

@app.route("/bow", methods = ['POST'])
def bow():
    global last_data
    data = json.loads(request.get_json())
    fname = f'data/{data["mac_address"]}{data["timestamp"]}.csv'
    with open(fname, 'a') as f:
        f.write("{},{},{}\n".format(data["time"], data["pressure1"], data["pressure2"]))
        f.close()
    last_data = f'{data["time"]},{data["pressure1"]},{data["pressure2"]}'
    return f'file_name:  {data["mac_address"]}{data["timestamp"]}\n'

@app.route("/csv", methods = ['GET'])
def get_csv():
    fname = request.args.get('file_name') + '.csv'
    files = os.listdir("bow_data")
    if fname in files:
        return send_file('data/' + fname,
                mimetype='text/csv',
                attachment_filename='data/' + fname,
                as_attachment=True)
    else:
        return abort(400)

@app.route("/last_data", methods = ['GET'])
def get_last_data():
    global last_data
    return last_data

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
