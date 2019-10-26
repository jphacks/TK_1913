from time import sleep
from datetime import datetime
import bluetooth
import json
from collections import deque
import requests
import threading
import sys
# import RPi.GPIO as GPIO
from dps310 import DPS310
from btxmt import BTServer


PORT = 1
RECV_SIZE = 1024
MY_ADDR = 'B8:27:EB:56:A1:68'


def connect_with_neck():
    global queue
    global bow_flag
    global bow_id
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
                    if bow_flag:
                        timestamp = datetime.today().timestamp()
                        data = {
                            "timestamp": bow_id,
                            "time": timestamp,
                            "pressure1": p_neck,
                            "pressure2": p_waist,
                            "mac_address": "b8:27:eb:a9:5e:97",
                        }
                        json_data = json.dumps(data)
                        queue.append(json_data)
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
    global bow_id
    while True:
        # if push switch
        print("gpio")
        bow_id = datetime.today().timestamp()
        bow_flag = True
        sleep(20)
        bow_flag = False
        sleep(20)

def post_json():
    global queue
    global bow_flag
    queue.clear()
    while True:
        if len(queue) > 0:
            json_data = queue.popleft()
            print(json_data)
            try:
                print("start")
                response = requests.post('http://ec2-13-115-229-32.ap-northeast-1.compute.amazonaws.com/bow', json=json_data)
                print(response)
                print("finish")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
        sleep(0.1)

if __name__ == '__main__':
    queue = deque()
    bow_flag = False
    bow_id = 0
    thread_1 = threading.Thread(target=connect_with_neck)
    thread_2 = threading.Thread(target=gpio)
    thread_3 = threading.Thread(target=post_json)
    thread_1.start()
    thread_2.start()
    thread_3.start()
