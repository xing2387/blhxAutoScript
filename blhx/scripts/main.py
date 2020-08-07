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
    return 1


def getScreenshot():
    global device
    getpic.downloadScreenshot("/tmp/sdafwer.jpg", device)
    return cv.imread("/tmp/sdafwer.jpg")


def findChapter(subchapterName):
    # goto first chapter by clicking last chapter btn 10 times
    s, e = splitSubchapterName(subchapterName)
    chapter = Configure.getChapter(s)
    page = chapter.pageIndex
    count = 12
    btnLeft = Configure.getButton("lastchapter")
    btnright = Configure.getButton("nextchapter")
    imgLeftBtn = cv.imread(btnLeft.path)
    imgRightBtn = cv.imread(btnright.path)
    sourceImg = getScreenshot()
    hasLeft, locL = matchTemplate.hasItem(sourceImg, imgLeftBtn, btnLeft.threshold)
    hasRight, locR = matchTemplate.hasItem(sourceImg, imgRightBtn, btnright.threshold)
    if hasLeft:
        funClickLeft = fpartial(click, x=locL[0][0], y=locL[0][1] - imgLeftBtn.shape[0], w=50, h=-90, deltaT=50)
    else:
        funClickLeft = None
    if hasRight:
        funClickRight = fpartial(click, x=locR[0][0], y=locR[0][1] - imgRightBtn.shape[0], w=50, h=-90, deltaT=50)
    else:
        funClickRight = None
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
            if funClickLeft:
                funClickLeft()
                count -= 1
        else:
            if funClickRight:
                funClickRight()
                count += 1
        time.sleep(2)
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
    hasLeft, loc = matchTemplate.hasItem(
        sourceImg, imgLeftBtn, btnLeft.threshold)
    hasRight, loc = matchTemplate.hasItem(
        sourceImg, imgRightBtn, btnright.threshold)
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
            print("find subchapter label " + template.path + ", attempt " + str(attempt))
            result, location = matchTemplate.hasItem(sourceImg, templateImg, template.threshold)
            if result:
                location = location[0]
                click(location[0], location[1], templateImg.shape[1]/2, templateImg.shape[0]/2, 70)
                time.sleep(2)
                break
            sourceImg = getScreenshot()
            time.sleep(2)
            attempt += 1
        if attempt < attemptTimes:
            time.sleep(2)
            return

        print("could not find subchapter label " + subchapterName)
        findChapter(subchapterName)
    except KeyError:
        print(subchapterName + " chapter configuration not found")
    # Configure.getSubchapters[]
    # pts = matchTemplate.matchSingleTemplate()


def gofight(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    click(pt[0], pt[1], 150, 60, 30)
    return 3


def shortEnemyPositionList(points, shortOrder):
    ''' shortOrder: see `bossDirect` of class `Subchapter` in configurehelper.py '''
    # points.sort(key=lambda x:[-x[0],-x[1]])
    pass


def findEnemies(sourceImg, enemyIconsImg, enemyIconsMask):
    # print(sourceImg.shape)
    rect = Rect(0, 0, sourceImg.shape[1], sourceImg.shape[0])
    locs = matchTemplate.matchMutiTemplateInRect(sourceImg, enemyIconsImg, 0.8, rect, masks=enemyIconsMask)
    shortEnemyPositionList(locs, 1)
    return locs


def clickToFight(pt):
    click(pt[0]+10, pt[1]+10, 60, 60, 80)

def isSubchapterScene():
    subTemplate = Configure.getScenes()['subchapter'].templates[0].path
    sourceImg = getScreenshot()
    locs = matchTemplate.matchSingleTemplate(sourceImg, cv.imread(subTemplate), 0.9)
    return len(locs) > 0
    

def subchapter(locations, sourceImg, subchapterName):
    s, e = splitSubchapterName(subchapterName)
    subchapter = Configure.getSubchapter(s, e)
    count = subchapter.fight
    enemyIconsImg = []
    enemyIconsMask = []
    iconCount = len(subchapter.enemyIcons)
    for enemyIcon in subchapter.enemyIcons[1:int(iconCount/2)]:
        enemyIconsImg.append(cv.imread(enemyIcon))
        print("=========== " + str(int(iconCount/2)) +", "+str(enemyIcon))
    for enemyIcon in subchapter.enemyIcons[int(iconCount/2)+1:]:
        enemyIconsMask.append(cv.imread(enemyIcon))
    bossIconImg = cv.imread(subchapter.enemyIcons[0])
    bossIconMask = cv.imread(subchapter.enemyIcons[int(iconCount/2)])
    bossLoc = findEnemies(sourceImg, [bossIconImg], [bossIconMask])
    if len(bossLoc) > 0:
        print("findBoss")
        clickToFight([bossLoc[0][0], bossLoc[0][1]])
        return 3
    while count > 0:
        print("subchapter")
        if not isSubchapterScene():
            return 3
        sourceImg = getScreenshot()
        locs = findEnemies(sourceImg, enemyIconsImg, enemyIconsMask)
        if len(locs) <= 0:
            # drag
            continue
        clickToFight([locs[-1][0], locs[-1][1]])
        time.sleep(7)
        count -= 1
    return 3


def formation(locations, sourceImg, subchapterName):
    locations = locations[0][0]
    print(locations)
    click(locations[0]+10, locations[1]+10, 330, 140, 80)


def fighting(locations, sourceImg, subchapterName):
    btnAutoFight = Configure.getButton("autofight")
    btnAutoFightImg = cv.imread(btnAutoFight.path)
    found, loc = matchTemplate.hasItem(sourceImg, btnAutoFightImg, btnAutoFight.threshold)
    if found:
        sourceImg = getScreenshot()
        found, loc = matchTemplate.hasItem(sourceImg, btnAutoFightImg, btnAutoFight.threshold)
    if found:
        click(70, 50, 270, 60, 80)
        time.sleep(3)
        click(230, 450, 200, 250, 70)
    time.sleep(50)
    scence, locations = scencehelper.witchScence(getScreenshot())
    while scence == 'fighting':
        time.sleep(10)
        scence, locations = scencehelper.witchScence(getScreenshot())
    time.sleep(4)
    if scence == 'victory':
        return victory(locations, sourceImg, subchapterName)
    else:
        return 5


def victory(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(5)
    return 6


def getitem(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(7)
    return 7


def getship(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(7)
    return 8


def battleend(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(7)
    return 3

def avoid(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(4)
    return 3


actionFunctions = {
    #主页面
    'home':         home,
    #选章节
    'precombat':    precombat,
    #选完章节后的立即前往，和舰队选择
    'gofight':      gofight,
    #遭遇伏击
    'avoid':        avoid,
    #进入第几章中
    'subchapter':   subchapter,
    #“编队”页面，点击进入“战斗”页
    'formation':    formation,
    #“战斗”页
    'fighting':     fighting,
    'victory':      victory,
    'getitem':      getitem,
    'getship':      getship,
    'battleend':    battleend
}


def splitSubchapterName(subchapterName):
    s, e = splitSubchapter(subchapterName)
    return 's' + s, 'e' + e


def splitSubchapter(subchapterName):
    return subchapterName.split('-')


def battle(subchapterName, preferSenceIndex=0):
    while True:
        sourceImg = getScreenshot()
        scence, locations = scencehelper.witchScence(sourceImg, preferSenceIndex)
        if scence:
            print(scence)
            actionFunctions[scence](locations, sourceImg, subchapterName)
        else:  # error, try again
            time.sleep(4)

device = None

def main(argv):
    global device
    opts, args = getopt.getopt(argv, "c:d:", ["chapter=", "device="])
    subchapterName = None
    for opt, arg in opts:
        if opt in ("-c", "--chapter"):
            subchapterName = arg
        elif opt in ("-d", "--device"):
            device = arg
            print("device "+str(device))
    # print(isSubchapterScene())
    getpic.screenshotStart(device)
    battle(subchapterName)

if __name__ == '__main__':
    main(sys.argv[1:])
