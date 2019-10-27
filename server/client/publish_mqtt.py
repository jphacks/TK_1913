import paho.mqtt.publish as publish
import time
import json
import random

data = {
    "time": time.time(),
    "pressure1": random.randrange(980, 1010),
    "pressure2": random.randrange(980, 1010),
    "mac_address" : "04:49:21:02:62:7e",
    "timestamp": time.time()
}
json_data = json.dumps(data)
print(json_data)

publish.single('topic', json_data, hostname='localhost', port=1883) 
