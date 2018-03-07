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
from functools import partial as fpartial
from configurehelper import Configure, Scene, Template, Rect
import matchTemplate


def click(x, y, w, h, deltaT):
    x = x + w * random.random()
    y = y + h * random.random()
    inputhelper.click(x, y, round(deltaT*random.random()))


def home(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    click(pt[0], pt[1], 150, 80, 30)
    time.sleep(2)
    battle(subchapterName, 1)


def getScreenshot():
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    return cv.imread("/tmp/sdafwer.jpg")


def findChapter(subchapterName):
    # goto first chapter by clicking last chapter btn 10 times
    s, e = splitSubchapterName(subchapterName)
    chapter = Configure.getChapter(s)
    page = chapter.pageIndex
    count = 10
    btnLeft = Configure.getButton("lastchapter")
    btnright = Configure.getButton("nextchapter")
    imgLeftBtn = cv.imread(btnLeft.path)
    imgRightBtn = cv.imread(btnright.path)
    sourceImg = getScreenshot()
    hasLeft, loc = matchTemplate.hasItemInRect(
        sourceImg, imgLeftBtn, btnLeft.threshold, btnLeft.rect)
    hasRight, loc = matchTemplate.hasItemInRect(
        sourceImg, imgRightBtn, btnright.threshold, btnright.rect)

    funClickLeft = fpartial(click, x=60, y=500, w=50, h=80, deltaT=50)
    funClickRight = fpartial(click, x=1810, y=500, w=50 + 15, h=80, deltaT=50)
    print("========================== " + str(hasLeft) +
          " ==== " + str(hasRight) + " ==========")
    if not hasLeft:
        print("btn lastChapter not found")
        count = 0
    if (not hasRight) and (not hasLeft):
        return
    print("========================== click left " + str(count) + " ==========")
    while (count > 0):
        clickLeft = (10 * random.random()) > 1
        if clickLeft:
            funClickLeft()
            time.sleep(1.5)
            count -= 1
        else:
            funClickRight()
            time.sleep(2)
            count += 1
    extraRight = round(3 * random.random())
    count = page + extraRight
    i = count
    print("========================== click right " + str(count) + " ==========")
    while (i > 0):
        clickRight = (10 * random.random()) > 1.5
        if clickRight:
            funClickRight()
            time.sleep(1.5)
            i -= 1
        else:
            funClickLeft()
            time.sleep(2)
            i = min(count, i + 1)
    count = extraRight
    sourceImg = getScreenshot()
    hasLeft, loc = matchTemplate.hasItemInRect(
        sourceImg, imgLeftBtn, btnLeft.threshold, btnLeft.rect)
    hasRight, loc = matchTemplate.hasItemInRect(
        sourceImg, imgRightBtn, btnright.threshold, btnright.rect)
    if not hasRight:
        print("btn lastChapter not found")
        count = 10 - page
    if (not hasRight) and (not hasLeft):
        return
    print("========================== click left " + str(count) + " ==========")
    while (count > -1):
        funClickLeft()
        time.sleep(1)
        count -= 1


def precombat(locations, sourceImg, subchapterName):
    print("locations: " + str(locations))
    s, e = splitSubchapterName(subchapterName)
    try:
        template = Configure.getSubchapter(s, e).labels[0]
        templateImg = cv.imread(template.path)
        attempt = 0
        attemptTimes = 2
        for x in range(attemptTimes):
            print("find subchapter label " +
                  template.path + ", attempt " + str(attempt))
            result, location = matchTemplate.hasItemInRect(
                sourceImg, templateImg, template.threshold, template.rect)
            if result:
                location = location[0]
                click(location[0], location[1],
                      template.rect.width/2, template.rect.height/2, 70)
                time.sleep(2)
                break
            sourceImg = getScreenshot()
            time.sleep(2)
            attempt += 1
        if attempt < attemptTimes:
            time.sleep(2)
            battle(subchapterName, 2)

        print("could not find subchapter label " + subchapterName)
        findChapter(subchapterName)
        battle(subchapterName)
    except KeyError:
        print(subchapterName + " chapter configuration not found")
    # Configure.getSubchapters[]
    # pts = matchTemplate.matchSingleTemplate()


def gofight(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    click(pt[0], pt[1], 150, 60, 30)
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
