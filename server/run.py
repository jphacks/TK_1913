from database import init_db
from database import db
from flask import Flask, request, send_file, abort, render_template
import json
from models import Bow
import os
import math
import csv
import normalize
import glob

app = Flask(__name__)
app.config.from_object('config.Development')
init_db(app)

@app.route("/")
def index():
    return "Hello"

@app.route("/bow", methods = ['POST'])
def bow():
    global last_data
    data_list = json.loads(request.get_json())
    for data in data_list:
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

@app.route("/bows")
def bows():
    path = "./data"
    bow_names = []
    bow_data = []
    for x in glob.glob(os.path.join(path, '*.csv')):
        tmp = os.path.relpath(x, path)
        bow_names.append(tmp)
        with open("./data/" + tmp, 'r') as f:
            bow_data = list(csv.reader(f))
    return render_template("index.html", message1 = bow_names, message2 = bow_data)

@app.route("/unity")
def unity():
    return "HElloooo"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
