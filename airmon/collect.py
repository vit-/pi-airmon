import time

import serial

from airmon import const
from airmon.storage import store_co2_level
from airmon.storage.models import bind_db


def mh_z19():
    cmd = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    with serial.Serial(
        '/dev/serial0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.0
    ) as ser:
        while True:
            ser.write(cmd)
            result = ser.read(9)
            if result:
                checksum = 0xFF - (sum(result[1:8]) % 256) + 0x01
                if checksum == result[8]:
                    value = result[2] * 256 + result[3]
                    yield value + const.mh_z19_drift


def collect():
    for value in mh_z19():
        store_co2_level(value)
        time.sleep(const.collect_interval_secs)


if __name__ == '__main__':
    print('Starting collection')
    bind_db()
    collect()
