from time import sleep
import bluetooth

from dps310 import DPS310
from btxmt import BTClient


ADDR = 'B8:27:EB:56:A1:68'
PORT = 1


def main():
    dps310 = DPS310()

    bt_client = BTClient(ADDR, PORT)
    bt_client.connect()
    while True:
        try:
            scaled_p = dps310.calcScaledPressure()
            scaled_t = dps310.calcScaledTemperature()
            p = dps310.calcCompPressure(scaled_p, scaled_t)
            bt_client.send(f'p{p}')
            sleep(0.1)
        except KeyboardInterrupt:
            bt_client.disconnect()
            break


if __name__ == '__main__':
    main()
