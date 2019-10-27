from database import init_db
from database import db
from flask import Flask, request, send_file, abort, render_template
from flask_mqtt import Mqtt
import json
from models import Bow
import os
import math
import csv
import normalize
import glob

app = Flask(__name__)
app.config.from_object('config.Development')
mqtt = Mqtt(app)
init_db(app)

# subscribe topic
mqtt.subscribe(app.config['MQTT_TOPIC'])

def get_filename(data):
    return f'data/{data["mac_address"]}{data["timestamp"]}.csv'

def format_data(data):
    return f'{data["time"]},{data["pressure1"]},{data["pressure2"]}'

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)
    formated = format_data(data)
    
    with open(get_filename(data), "a") as f:
        f.write(f'{formated}\n')
    
    global last_data
    last_data = formated

@app.route("/")
def index():
    bows = db.session.query(Bow.id, Bow.created_at).all()
    return render_template("bows.html", bows=bows)

@app.route("/bow", methods = ['POST'])
def bow():
    global last_data
    data_list = json.loads(request.get_json())

    for data in data_list:
        formated = format_data(data)
        last_data = formated
        with open(get_filename(data), 'a') as f:
            f.write(f'{formated}\n')
    
    return ('', 200)

@app.route("/register", methods = ['GET'])
def register():
    data = {
        "mac_address": request.args.get("mac_address"),
        "timestamp": request.args.get("timestamp")
    }
    fname = get_filename(data)

    bow = Bow()
    bow.timestamp = data["timestamp"]
    bow.macaddress = data["mac_address"]
    bow.path = fname
    db.session.add(bow)
    db.session.commit()
    
    try:
        normalize.normalize(fname)
    except FileNotFoundError:
        return ('', 404)

    return ('', 200)

@app.route("/csv", methods = ['GET'])
def get_csv():
    bow_id = request.args.get('bow_id')
    bow = db.session.query(Bow).filter(Bow.id==bow_id).first()
    file_path = bow.path
    normalized_path = f'normalized_data/{file_path.split("/")[1]}'

    if os.path.exists(normalized_path):
        return send_file(
            normalized_path,
            mimetype='text/csv',
            attachment_filename=normalized_path,
            as_attachment=True
        )
    else:
        return abort(400)

@app.route("/last_data", methods = ['GET'])
def get_last_data():
    global last_data
    return last_data

@app.route("/unity")
def unity():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
