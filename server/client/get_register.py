import time
import requests

def register():
    url = "http://localhost:5000"
    data = {
        "timestamp": time.time(),
        "mac_address": "ff:ff:ff:ff:ff:ff"
    }
    response = requests.get(f'{url}/register?timestamp={data["timestamp"]}&mac_address={data["mac_address"]}')
    print(response)

register()
