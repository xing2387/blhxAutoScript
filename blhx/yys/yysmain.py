#! /usr/bin/env python3

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
import time
from functools import partial as fpartial
from configurehelper import Configure, Scene, Template, Rect
import matchTemplate


def click(x, y, w, h, deltaT):
    print("click " + str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h))
    x = x + w * random.random()
    y = y + h * random.random()
    inputhelper.click(x, y, round(deltaT*random.random()))

def clickBtn(btn, xy=None):
    if not xy:
        click(btn.rect.x, btn.rect.y, btn.rect.width, btn.rect.height, 50)
    else:
        click(xy[0], xy[1], btn.rect.width, btn.rect.height, 50)
    

def showimg(img):
    cv.imshow("image1", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def getScreenshot():
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    return cv.imread("/tmp/sdafwer.jpg")

def findBtn(sourceImg, btn):
    btnImg = cv.imread(btn.path)
    return matchTemplate.hasItem(sourceImg, btnImg, btn.threshold)

def home(locations, sourceImg, subchapterName):
    btnExplorer = Configure.getButton("explore")
    found, loc = findBtn(sourceImg, btnExplorer)
    if found:
        clickBtn(btnExplorer, [loc[0][0], loc[0][1]])
    time.sleep(2)

def explore(locations, sourceImg, chapterName):
    chapterLabel = Configure.getChapter(chapterName).labels[0]
    print(chapterLabel)
    None

actionFunctions = {
    'home':         home,
    'explore':    explore
}

def battle(chapterName, preferSenceIndex=0):
    while True:
        sourceImg = getScreenshot()
        scence, locations = scencehelper.witchScence(sourceImg, preferSenceIndex)
        if scence:
            print(scence)
            actionFunctions[scence](locations, sourceImg, chapterName)
        else:  # error, try again
            time.sleep(4)

def main(argv):
    getpic.screenshotStart()
    opts, args = getopt.getopt(argv, "c:", ["chapter="])
    for opt, arg in opts:
        if opt in ("-c", "--chapter"):
            battle(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
