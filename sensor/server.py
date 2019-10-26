from time import sleep
from datetime import datetime
import bluetooth
import json

from dps310 import DPS310
from btxmt import BTServer


PORT = 1
RECV_SIZE = 1024
MY_ADDR = 'B8:27:EB:56:A1:68'


def main():
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

                    timestamp = datetime.today().timestamp()

                    data = {'timestamp': timestamp,
                            'p_waist': p_waist, 'p_neck': p_neck}
                    json_data = json.dumps(data)
                    print(json_data)
                    sleep(0.1)
                except bluetooth.btcommon.BluetoothError:
                    break
                except KeyboardInterrupt:
                    bt_server.disconnect()
                    break
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
