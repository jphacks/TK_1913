import urllib.request, json
import time

def start():
    url = "http://localhost:5000/register"
    method = "GET"
    headers = { "Content-Type": "application/json" }
    data = {
        "timestamp": time.time(),
        "mac_address": "ff:ff:ff:ff:ff:ff"
    }
    json_data = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)

start()
