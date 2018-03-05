#! /usr/bin/env python3
'''

'''

from __future__ import print_function
import os
import sys
import getopt
import requests
import cv2 as cv
import scencehelper
import getpic
import inputhelper
import random
from configurehelper import Configure, Scene, Template, Rect
import matchTemplate

def home(locations, sourceImg):
    pt = locations[0][0]
    x = pt[0] + 150 * random.random()
    y = pt[1] + 80 * random.random()
    inputhelper.click(x, y, round(30*random.random()))

def precombat(locations, sourceImg):
    pts = matchTemplate.matchSingleTemplate()
    


actionFunctions = {
    'home': home,
    'precombat': precombat
}

def battle(enemyIcons):
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    sourceImg = cv.imread("/tmp/sdafwer.jpg")
    scence, locations = scencehelper.witchScence(sourceImg)
    if scence:
        print(scence)
        actionFunctions[scence](locations, sourceImg)

def main(argv):
    getpic.rootScreenshotStart()
    opts, args = getopt.getopt(argv, "c:", ["chapter="])
    for opt, arg in opts:
        print(opts)
        if opt in ("-c", "--chapter"):
            s, e = arg.split('-')
            icons = Configure.getEnemyIcons('s'+s, 'e'+e)
            battle(icons)

if __name__ == '__main__':
    main(sys.argv[1:])