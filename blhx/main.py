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
import time
from configurehelper import Configure, Scene, Template, Rect
import matchTemplate


def home(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    x = pt[0] + 150 * random.random()
    y = pt[1] + 80 * random.random()
    inputhelper.click(x, y, round(30*random.random()))
    time.sleep(2)
    battle(subchapterName, 1)

def getScreenshot():
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    return cv.imread("/tmp/sdafwer.jpg")

def precombat(locations, sourceImg, subchapterName):
    print("locations: " + str(locations))
    s, e = splitSubchapterName(subchapterName)
    try:
        template = Configure.getSubchapter(s, e).labels[0]
        templateImg = cv.imread(template.path)
        attempt = 0
        attemptTimes = 4
        for x in range(attemptTimes):
            print("find subchapter label " +
                  template.path + ", attempt " + str(attempt))
            result, location = matchTemplate.hasItemInRect(
                sourceImg, templateImg, template.threshold, template.rect)
            if result:
                location = location[0]
                x = location[0] + random.random() * (template.rect.width/2)
                y = location[1] + random.random() * (template.rect.height/2)
                inputhelper.click(x, y, round(70 * random.random()))
                time.sleep(2)
                break
            sourceImg = getScreenshot()
            time.sleep(2)
            attempt += 1
        if attempt < attemptTimes:
            time.sleep(2)
            battle(subchapterName, 2)
            
        print("could not find subchapter label " + subchapterName)
        battle(subchapterName)
    except KeyError:
        print(subchapterName + " chapter configuration not found")
    # Configure.getSubchapters[]
    # pts = matchTemplate.matchSingleTemplate()


def gofight(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    x = pt[0] + 150 * random.random()
    y = pt[1] + 60 * random.random()
    inputhelper.click(x, y, round(30*random.random()))
    battle(subchapterName, 3)

def subchapter(locations, sourceImg, subchapterName):
    pass


actionFunctions = {
    'home': home,
    'precombat': precombat,
    'gofight': gofight,
    'subchapter': subchapter
}


def splitSubchapterName(subchapterName):
    s, e = splitSubchapter(subchapterName)
    return 's' + s, 'e' + e


def splitSubchapter(subchapterName):
    return subchapterName.split('-')


def battle(subchapterName, preferSenceIndex=0):
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    sourceImg = cv.imread("/tmp/sdafwer.jpg")
    # s, e = splitSubchapterName(subchapterName)
    # icons = Configure.getEnemyIcons(s, e)
    scence, locations = scencehelper.witchScence(sourceImg, preferSenceIndex)
    if scence:
        print(scence)
        actionFunctions[scence](locations, sourceImg, subchapterName)
    else:  # error, try again
        time.sleep(2)
        battle(subchapterName)


def main(argv):
    getpic.rootScreenshotStart()
    opts, args = getopt.getopt(argv, "c:", ["chapter="])
    for opt, arg in opts:
        if opt in ("-c", "--chapter"):
            battle(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
