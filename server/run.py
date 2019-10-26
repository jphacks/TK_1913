from database import init_db
from database import db
from flask import Flask, request, send_file, abort
import json
from models import Bow
import os
import math
import csv
import normalize

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

@app.route("/end", methods = ['GET'])
def end():
    fname = f'data/{request.args.get("mac_address")}{request.args.get("timestamp")}.csv'
    normalize.normalize(fname)
    return "Success normalization!"

@app.route("/csv", methods = ['GET'])
def get_csv():
    fname = request.args.get('file_name') + '.csv'
    files = os.listdir("normalized_data")
    if fname in files:
        return send_file('normalized_data/' + fname,
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
