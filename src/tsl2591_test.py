#!/usr/bin/env python3

from python_tsl2591 import tsl2591
import time

if __name__ == '__main__':

    tsl = tsl2591()  # initialize
    # full, ir = tsl.get_full_luminosity()  # Read raw values (full spectrum and infared spectrum).
    # lux = tsl.calculate_lux(full, ir)  # Convert raw values to Lux.

    while True:
        print(tsl.get_current()) # Return object with all values.
        # print (lux, full, ir)
        time.sleep(2)
