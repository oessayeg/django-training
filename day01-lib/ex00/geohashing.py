#!/usr/bin/env python3

import antigravity
import sys

if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            raise Exception("Program needs latitude, longitude and DJIA")
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        djia = sys.argv[3].encode()

        antigravity.geohash(latitude, longitude, djia)
    except Exception as e:
        print(e)
