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


def home(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    x = pt[0] + 150 * random.random()
    y = pt[1] + 80 * random.random()
    inputhelper.click(x, y, round(30*random.random()))


def precombat(locations, sourceImg, subchapterName):
    print("locations: " + str(locations))
    s, e = splitSubchapterName(subchapterName)
    try:
        templateFile = Configure.getChapterLabels()[s].path
        templateImg = cv.imread(templateFile)
        if matchTemplate.hasItem()
    except KeyError:
        print(subchapterName + " chapter configuration not found")
    # Configure.getSubchapters[]
    # pts = matchTemplate.matchSingleTemplate()


actionFunctions = {
    'home': home,
    'precombat': precombat
}


def splitSubchapterName(subchapterName):
    s, e = splitSubchapter(subchapterName)
    return 's' + s, 'e' + e


def splitSubchapter(subchapterName):
    return subchapterName.split('-')


def battle(subchapterName):
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    sourceImg = cv.imread("/tmp/sdafwer.jpg")
    # s, e = splitSubchapterName(subchapterName)
    # icons = Configure.getEnemyIcons(s, e)
    scence, locations = scencehelper.witchScence(sourceImg)
    if scence:
        print(scence)
        actionFunctions[scence](locations, sourceImg, subchapterName)


def main(argv):
    getpic.rootScreenshotStart()
    opts, args = getopt.getopt(argv, "c:", ["chapter="])
    for opt, arg in opts:
        if opt in ("-c", "--chapter"):
            battle(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
