# https://gist.github.com/UedaTakeyuki/bfe8b20c80e6f09c7105
import time

import serial

from airmon import const
from airmon.storage import store_co2_level


def mh_z19():
    with serial.Serial(
        '/dev/ttyAMA0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.0
    ) as ser:
        while True:
            ser.write("\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            s = ser.read(9)
            if s[0] == "\xff" and s[1] == "\x86":
                val = ord(s[2]) * 256 + ord(s[3])
                yield val


def collect():
    for value in mh_z19():
        store_co2_level(value)
        time.sleep(const.sample_interval_secs)


if __name__ == '__main__':
    collect()
