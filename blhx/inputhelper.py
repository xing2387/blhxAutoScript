#! /usr/bin/env python3

import os
import requests
import time
import sys


def click(x, y, deltaTime):
    ''' request like "http://127.0.0.1:53516/sendevent?type=click&clientX=300&clientY=400&downDelta=50"
        Args:
            x, y (float)       
            deltaTime (long): time bewteen pointer up an down
    '''
    params = "type=click&clientX=%(x)f&clientY=%(y)f&downDelta=%(deltaTime)d" % {
        'x': x, 'y': y, 'deltaTime': deltaTime}
    print("click " + params)
    req = requests.get('http://127.0.0.1:53516/sendevent?' + params)
    print(req)


if __name__ == '__main__':
    click(float(sys.argv[1]), float(sys.argv[2]), 56)