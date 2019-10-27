import urllib.request, json
import time
import random
import requests

def random_p():
    p1 = random.randrange(0, 2000)
    p2 = random.randrange(0, 2000)
    return p1, p2

def create_data():
    P = random_p()
    p1 = P[0]
    p2 = P[1]
    data = {
        "time": time.time(),
        "pressure1": p1,
        "pressure2": p2,
        "mac_address" : "04:49:21:02:62:7e",
        "timestamp": timestamp
    }
    return data

def send(timestamp):
    url = "http://localhost:5000"
    data = [create_data() for _ in range(10)]

    json_data = json.dumps(data).encode("utf-8")
    requests.post(f'{url}/bow', json=json_data)

timestamp = time.time()
send(timestamp)
