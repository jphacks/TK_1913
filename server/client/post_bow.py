import urllib.request, json
import time
import random


def random_p():
    p1 = random.randrange(0, 2000)
    p2 = random.randrange(0, 2000)
    return p1, p2

def send(timestamp):
    url = "http://localhost:8080/bow"
    method = "POST"
    headers = { "Content-Type": "application/json" }
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

    json_data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)

timestamp = time.time()
send(timestamp)
