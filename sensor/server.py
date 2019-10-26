from time import sleep
from datetime import datetime
import bluetooth
import json
import requests
import threading
import RPi.GPIO as GPIO
from dps310 import DPS310
from btxmt import BTServer


PORT = 1
RECV_SIZE = 1024
MY_ADDR = 'B8:27:EB:56:A1:68'

PIN = 21
TIMEOUT = 3000 # mill sec

def connect_with_neck():
    global data_list
    global bow_flag
    global start_flag
    global calibration_flag
    global offset_p
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
                    p_waist += offset_p

                    if bow_flag:
                        timestamp = datetime.today().timestamp()
                        if start_flag:
                            bow_id = timestamp
                            standard_p_neck = p_neck
                            start_flag = False
                        else:
                            if timestamp - bow_id > 2 and p_neck < standard_p_neck + 0.1:
                                bow_flag = False
                        data = {
                            "timestamp": bow_id,
                            "time": timestamp,
                            "pressure1": p_neck,
                            "pressure2": p_waist,
                            "mac_address": "b8:27:eb:a9:5e:97",
                        }
                        data_list.append(data)
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
                print('Calibration')

        except Exception as e:
            print(e)
            print("gpio")

def post_json():
    global data_list
    global bow_flag
    while True:
        if len(data_list) > 0:
            json_data, data_list = json.dumps(data_list), []
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
    data_list = []
    bow_flag = False
    start_flag = False
    calibration_flag = False
    offset_p = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    thread_1 = threading.Thread(target=connect_with_neck)
    thread_2 = threading.Thread(target=gpio)
    thread_3 = threading.Thread(target=post_json)
    thread_1.start()
    thread_2.start()
    thread_3.start()
