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

x = [440.000000, 443.16248, 444.000000, 448.000000, 454.000000, 459.000000, 
    466.000000, 470.444, 474.000000, 483.000000, 493.000000, 493.6268, 503.000000, 
    512.000000, 517.1772, 522.000000, 533.000000, 545.0766, 547.000000, 562.0, 562.0]
y = [1468.0, 1468.0, 1468.000000, 1468.000000, 1468.000000, 1468.000000, 1468.000000, 1468.0, 
    1468.000000, 1468.000000, 1468.000000, 1468.0, 1468.000000, 1468.000000, 1468.0, 
    1468.000000, 1468.000000, 1472.3131, 1473.000000, 1477.0, 1477.0]
print(len(x))
print(len(y))
def draw():
    plt.plot(range(len(y)), y, marker='o', mec='r', mfc='w',label=u'y=x^2')
    plt.legend()
    plt.xticks(range(len(y)), x, rotation=45)
    plt.margins(0)
    plt.show()

def main():
    if len(sys.argv) <= 1:
        return
    if sys.argv[1] == "click":
        click(float(sys.argv[2]), float(sys.argv[3]), 56)
    elif sys.argv[1] == "plt":
        draw()



if __name__ == '__main__':
    main()