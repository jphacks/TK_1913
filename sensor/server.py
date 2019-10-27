from time import sleep
from datetime import datetime
import bluetooth
import json
import requests
import threading
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from collections import deque
from dps310 import DPS310
from btxmt import BTServer


PORT = 1
RECV_SIZE = 1024
WF_ADDR = 'b8:27:eb:a9:5e:97'

PIN = 21
TIMEOUT = 3000 # milli sec

URL = 'http://komachi.hongo.wide.ad.jp'

MQTT_HOST = 'komachi.hongo.wide.ad.jp'
MQTT_PORT = 1883

def connect_with_neck():
    global data_list
    global bow_flag
    global start_flag
    global calibration_flag
    global offset_p
    global prev_p_neck
    global bow_id_queue
    global end_flag
    dps310 = DPS310()

    bt_server = BTServer(PORT)

    while True:
        addr = bt_server.accept()

        try:
            while True:
                try:
                    scaled_p = dps310.calcScaledPressure()
                    scaled_t = dps310.calcScaledTemperature()
                    p_waist = dps310.calcCompPressure(scaled_p, scaled_t)

                    recv_data = bt_server.recv(RECV_SIZE).decode()
                    p_neck = float(recv_data.split('p')[-1])

                    if calibration_flag:
                        offset_p = p_neck - p_waist
                        calibration_flag = False
                        print(f'neck:{p_neck},waist:{p_waist},offset:{offset_p}')
                    p_waist += offset_p
                    
                    timestamp = datetime.today().timestamp()
                    if bow_flag:
                        if start_flag:
                            bow_id = timestamp
                            bow_id_queue.append(bow_id)
                            standard_p_neck = p_neck
                            start_flag = False
                        else:
                            if (timestamp - bow_id > 2 and
                                p_neck < standard_p_neck + 0.5):
                                bow_flag = False
                                end_flag = True

                        data = {
                            "timestamp": bow_id,
                            "time": timestamp,
                            "pressure1": p_neck,
                            "pressure2": p_waist,
                            "mac_address": WF_ADDR,
                        }
                        json_data = json.dumps(data)
                        client.publish('bow/bow', json_data)
                        data_list.append(data)
                        print(f'Neck: {p_neck}, Waist: {p_waist}')
                        v = p_neck - prev_p_neck
                        prev_p_neck = p_neck
                        print(v)
                    else:
                        data = {
                            "timestamp": timestamp,
                            "time": timestamp,
                            "pressure1": p_neck,
                            "pressure2": p_waist,
                            "mac_address": WF_ADDR,
                        }
                        json_data = json.dumps(data)
                        client.publish('bow', json_data)
                    sleep(0.1)
                except bluetooth.btcommon.BluetoothError:
                    break
                except KeyboardInterrupt:
                    bt_server.disconnect()
                    break
        except KeyboardInterrupt:
            break

def gpio():
    global bow_flag
    global start_flag
    global calibration_flag
    while True:
        try:
            GPIO.wait_for_edge(PIN, GPIO.FALLING)
            pin = GPIO.wait_for_edge(PIN, GPIO.RISING, timeout=TIMEOUT)
            if pin is not None:
                bow_flag = True
                start_flag = True
            else:
                calibration_flag = True

        except Exception as e:
            print(e)

def post_json():
    global data_list
    global bow_flag
    while True:
        if len(data_list) > 0:
            data_list = []
        sleep(0.1)

def get():
    global end_flag
    global data_list
    global bow_id_queue
    while True:
        sleep(1)
        if len(data_list) > 0:
            if data_list[0]["timestamp"] != bow_id_queue[0]:
                get_bow_id = bow_id_queue.popleft()
                try:
                    response = requests.get(f'{URL}/register?timestamp={get_bow_id}&mac_address={WF_ADDR}')
                    print(response)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    # print(e)
                    pass
                end_flag = False
        if end_flag and len(data_list) == 0:
            end_flag = False
            get_bow_id = bow_id_queue.popleft()
            print(get_bow_id)
            try:
                response = requests.get(f'{URL}/register?timestamp={get_bow_id}&mac_address={WF_ADDR}')
                print(response)
            except KeyboardInterrupt:
                break
            except Exception as e:
                # print(e)
                pass


if __name__ == '__main__':
    data_list = []
    bow_flag = False
    start_flag = False
    end_flag = False
    calibration_flag = False
    offset_p = 0
    prev_p_neck = 0
    bow_id_queue = deque()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
    thread_1 = threading.Thread(target=connect_with_neck)
    thread_2 = threading.Thread(target=gpio)
    thread_3 = threading.Thread(target=post_json)
    thread_4 = threading.Thread(target=get)
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
