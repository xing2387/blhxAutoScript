#! /usr/bin/env python3

from __future__ import print_function
import os
import requests
import time
import sys
import matplotlib.pyplot as plt
import random


def click(x, y, deltaTime):
    ''' request like "http://127.0.0.1:53516/sendevent?type=click&clientX=300&clientY=400&downDelta=50"
                        
        Args:
            x, y (float)       
            deltaTime (long): time bewteen pointer up an down
    '''
    params = "type=click&clientX=%(x)f&clientY=%(y)f&downDelta=%(deltaTime)d" % {
        'x': x, 'y': y, 'deltaTime': deltaTime}
    print("click " + params)
    req = requests.get('http://127.0.0.1:50088/sendevent?' + params)
    print(req)

def drag(startx, starty, endx, endy):
    # http://127.0.0.1:50088/sendevent?type=drag&path=[500,500,700,900]
    params = "type=drag&path=[%(startx)d,%(starty)d,%(endx)d,%(endy)d]" % {
        'startx': startx, 'starty': starty, 'endx': endx, 'endy': endy}
    print("drag " + params)
    req = requests.get('http://127.0.0.1:50088/sendevent?' + params)
    print(req)

def dragRandom(times=1):
    withNone = ["up","down","left","right", "None", "None"]
    withoutNone = ["up","down","left","right"]
    aa = random.choice(withNone)
    if aa == "None":
        bb = random.choice(withoutNone)
    else:
        bb = random.choice(withNone)
    directory = aa + "|" + bb
    print("dragRandom " + directory)
    while times > 0:
        times -= 1
        dragWithDirectory(directory=directory)
        time.sleep(1)

def dragWithDirectory(directory="up", screenW=1920, screenH=1080):
    '''
    directory : up, down, left, right. 可组合
    '''
    shortEdge = min(screenW, screenH)
    distY = distX = shortEdge * 0.1 * (random.random() - 0.5)
    distH = screenW * (0.2 + random.random() * 0.15)
    distV = screenH * (0.3 + random.random() * 0.2)
    startX = screenW * (0.5 + (random.random() - 0.5) * 0.2)
    startY = screenH * (0.5 + (random.random() - 0.5) * 0.2)
    if "down" in directory:
        distY = -distV
    if "left" in directory:
        distX = -distH
    if "up" in directory:
        distY = distV
    if "right" in directory:
        distX = distH
    drag(startX, startY, startX + distX, startY + distY)


def main():
    if len(sys.argv) <= 1:
        return
    if sys.argv[1] == "click":
        click(float(sys.argv[2]), float(sys.argv[3]), 56)



if __name__ == '__main__':
    main()