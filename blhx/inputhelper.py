#! /usr/bin/env python3

from __future__ import print_function
import os
import requests
import time
import sys
import matplotlib.pyplot as plt


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

def main():
    if len(sys.argv) <= 1:
        return
    if sys.argv[1] == "click":
        click(float(sys.argv[2]), float(sys.argv[3]), 56)



if __name__ == '__main__':
    main()