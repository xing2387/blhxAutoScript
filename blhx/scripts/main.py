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

#===============记录================
battleCount = {}
bossCount = {}
#===================================

def click(x, y, w, h, deltaT):
    x = x + w * random.random()
    y = y + h * random.random()
    inputhelper.click(x, y, round(deltaT*random.random()))


def home(locations, sourceImg, subchapterName):
    pt = locations[0][0]
    click(pt[0], pt[1], 150, 80, 30)
    time.sleep(2)
    return 'precombat'


def getScreenshot():
    global device
    getpic.downloadScreenshot("/tmp/sdafwer.jpg", device)
    return cv.imread("/tmp/sdafwer.jpg")

def isFleet1(sourceImg = None):
    if sourceImg is None:
        sourceImg = getScreenshot()
    template = Configure.getButton("flat1")
    hasItem, loc = matchTemplate.hasItem(sourceImg, template.getImg(), template.threshold)
    return hasItem

def isFleet2(sourceImg = None):
    if sourceImg is None:
        sourceImg = getScreenshot()
    template = Configure.getButton("flat2")
    hasItem, loc = matchTemplate.hasItem(sourceImg, template.getImg(), template.threshold)
    return hasItem

def findChapter(subchapterName):
    # goto first chapter by clicking last chapter btn 10 times
    s, e = splitSubchapterName(subchapterName)
    sourceImg = getScreenshot()
    chapter = Configure.getChapter(s)
    template = chapter.labels[0]
    # templateImg = cv.imread(template.path)
    hasChapter, loc = matchTemplate.hasItem(sourceImg, template.getImg(), template.threshold)
    if hasChapter:
        click(loc[0][0], loc[0][1], 20, 20, 50)
        return

    page = chapter.pageIndex
    count = 12
    btnLeft = Configure.getButton("lastchapter")
    btnright = Configure.getButton("nextchapter")
    imgLeftBtn = btnLeft.getImg()
    imgRightBtn = btnright.getImg()
    hasLeft, locL = matchTemplate.hasItem(sourceImg, imgLeftBtn, btnLeft.threshold)
    hasRight, locR = matchTemplate.hasItem(sourceImg, imgRightBtn, btnright.threshold)
    if hasLeft:
        funClickLeft = fpartial(click, x=locL[0][0], y=locL[0][1] - imgLeftBtn.shape[0], w=50, h=-90, deltaT=50)
    else:
        funClickLeft = fpartial(print, "")
    if hasRight:
        funClickRight = fpartial(click, x=locR[0][0], y=locR[0][1] - imgRightBtn.shape[0], w=50, h=-90, deltaT=50)
    else:
        funClickRight = fpartial(print, "")
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
            count -= 1
        else:
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
    hasLeft, loc = matchTemplate.hasItem(sourceImg, imgLeftBtn, btnLeft.threshold)
    hasRight, loc = matchTemplate.hasItem(sourceImg, imgRightBtn, btnright.threshold)
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
        templateImg = template.getImg()
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
            return 'gofight'

        print("could not find subchapter label " + subchapterName)
        findChapter(subchapterName)
    except KeyError:
        print(subchapterName + " chapter configuration not found")
    return 'precombat'
    # Configure.getSubchapters[]
    # pts = matchTemplate.matchSingleTemplate()


def gofight(locations, sourceImg, subchapterName):
    global lastScene
    pt = locations[0][0]
    click(pt[0], pt[1], 150, 60, 30)
    time.sleep(5)
    if lastScene == 'precombat':
        return 'gofight'
    else:
        return 'subchapter'


def shortEnemyPositionList(points, shortOrder):
    ''' shortOrder: see `bossDirect` of class `Subchapter` in configurehelper.py '''
    # points.sort(key=lambda x:[-x[0],-x[1]])
    pass


def findEnemies(sourceImg, enemyIconsImg, enemyIconsMask, threshold=0.9):
    # print(sourceImg.shape)
    global fieldRect
    locs = matchTemplate.matchMutiTemplateInRect(sourceImg, enemyIconsImg, threshold, fieldRect, masks=enemyIconsMask)
    shortEnemyPositionList(locs, 1)
    return locs


def clickToFight2(pt, offset, size):
    global fieldRect
    global screenSize
    x = (pt[0] + offset[0]) + size[0] * random.random()
    y = (pt[1] + offset[1]) + size[1] * random.random()
    centerX = screenSize - 50 + (100 * random.random())
    centerY = screenSize - 50 + (100 * random.random())
    if x < fieldRect.x or x > (fieldRect.x + fieldRect.width):
        dist = 90 + 30 * random.random()
        if x > fieldRect.x:
            dist = -dist
        inputhelper.drag(centerX, centerY, centerX + dist, centerY + (20 * random.random()))
        return False
    if y < fieldRect.y or y > (fieldRect.y + fieldRect.height):
        dist = 90 + 30 * random.random()
        if y > fieldRect.y:
            dist = -dist
        inputhelper.drag(centerX, centerY, centerX + (20 * random.random()), centerY + dist)
        return False
    inputhelper.click(x, y, round(80*random.random()))
    return True


def clickToFight(pt):
    return clickToFight2(pt, (40, 60), (90, 60))

def isSubchapterScene(sourceImg=None):
    if sourceImg is None:
        sourceImg = getScreenshot()
    subTemplate = Configure.getScenes()['subchapter'].templates[0].path
    locs = matchTemplate.matchSingleTemplate(sourceImg, cv.imread(subTemplate), 0.9)
    return len(locs) > 0

def findSelfLocation(sourceImg=None):
    if sourceImg is None:
        sourceImg = getScreenshot()
    selfIcon = Configure.getButton("self")
    hasItem, location = matchTemplate.hasItem(sourceImg, cv.imread(selfIcon.path), selfIcon.threshold)
    return location

def isSelfMoved(lastLoc, selfLoc=None):
    if selfLoc is None:
        selfLoc = findSelfLocation(sourceImg)
        if len(selfLoc) > 0:
            selfLoc = selfLoc[-1]
    if selfLoc is not None:
        print("isSelfMoved " + str(lastLoc[0] - selfLoc[0]) + ", " + str(lastLoc[1] - selfLoc[1]))
        return abs(lastLoc[0] - selfLoc[0]) > 50 or abs(lastLoc[1] - selfLoc[1]) > 50
    else:
        return None

def clickBotton(name, sourceImg = None):
    if sourceImg is None:
        sourceImg = getScreenshot()
    btn = Configure.getButton(name)
    hasItem, loc = matchTemplate.hasItem(sourceImg, btn.getImg(), btn.threshold)
    if hasItem:
        click(x=loc[0][0], y=loc[0][1], w=50, h=50, deltaT=50)
        time.sleep(3)
    
def switchFleet(sourceImg = None):
    global fleet
    if sourceImg is None:
        sourceImg = getScreenshot()
    if ((fleet == 1) and isFleet1(sourceImg)) or ((fleet == 2) and isFleet2(sourceImg)):
        return False
    else:
        clickBotton("switchfleet", sourceImg)
        return True

minDistance = 200
def subchapter(locations, sourceImg, subchapterName):
    global limitMove
    if switchFleet(sourceImg):
        sourceImg = getScreenshot()
    s, e = splitSubchapterName(subchapterName)
    subchapter = Configure.getSubchapter(s, e)
    count = subchapter.fight
    enemyIconsImg = []
    enemyIconsMask = []

    bossIconImg = []
    bossIconMask = []

    iconCount = len(subchapter.enemyIcons)
    for enemyIcon in subchapter.enemyIcons[0:int(iconCount/2)]:
        if "boss" in enemyIcon:
            bossIconImg.append(cv.imread(enemyIcon))
        else:
            enemyIconsImg.append(cv.imread(enemyIcon))
    for enemyIcon in subchapter.enemyIcons[int(iconCount/2):]:
        if "boss" in enemyIcon:
            bossIconMask.append(cv.imread(enemyIcon))
        else:
            enemyIconsMask.append(cv.imread(enemyIcon))
    enemyLoc = None
    limitCount = 3
    while count > 0:
        count -= 1
        print("subchapter")
        sourceImg = getScreenshot()
        if not isSubchapterScene(sourceImg):
            bb = Configure.getScenes()["formation"].templates[0]
            hasItem, aa = matchTemplate.hasItem(sourceImg, cv.imread(bb.path), bb.threshold)
            if hasItem:
                return 'formation'
            else:
                time.sleep(10)
                return 'battleend'
        locs = []

        offset = (40, 60)
        size = (90, 60)
        if (not limitMove) or (enemyLoc is None):
            iconIndex = 0
            while len(locs) <= 0 and iconIndex < len(bossIconImg):
                locs = findEnemies(sourceImg, [bossIconImg[iconIndex]], [bossIconMask[iconIndex]])
                offset = (0, 0)
                size = (bossIconImg[iconIndex].shape[1]-10, bossIconImg[iconIndex].shape[0]-10)
                iconIndex += 1
            iconIndex = 0
            if len(locs) <= 0:
                locs = findEnemies(sourceImg, enemyIconsImg, enemyIconsMask)
                offset = (40, 60)
                size = (90, 60)
            # while len(locs) <= 0 and iconIndex < len(enemyIconsImg):
            #     locs = findEnemies(sourceImg, [enemyIconsImg[iconIndex]], [enemyIconsMask[iconIndex]])
            #     iconIndex += 1
            #     offset = (40, 60)
            #     size = (90, 60)
            if len(locs) <= 0:
                inputhelper.dragRandom(3)
                continue
            enemyLoc = locs[-1]
        if limitMove:
            lastLoc = findSelfLocation(sourceImg)
            if len(lastLoc) <= 0:
                print("self not found")
                inputhelper.dragRandom()
                enemyLoc = None
                continue
            else:
                lastLoc = lastLoc[0]
        while True:
            if not clickToFight2(enemyLoc, offset, size):
                time.sleep(2)
                break
            time.sleep(1)
            sourceImg = getScreenshot()
            bb = Configure.getButton("outrange")
            hasItem, aa = matchTemplate.hasItem(sourceImg, cv.imread(bb.path), bb.threshold)
            if hasItem:
                break
            bb = Configure.getButton("blockout")
            hasItem, aa = matchTemplate.hasItem(sourceImg, cv.imread(bb.path), bb.threshold)
            if hasItem:
                locs.remove(enemyLoc)
                if len(locs) <= 0:
                    inputhelper.dragRandom(3)
                    time.sleep(1)
                    break
                else:
                    enemyLoc = locs[-1]
                    continue
            else:
                break
                

        time.sleep(5)

        while limitMove:
            selfLoc = findSelfLocation(sourceImg)
            if len(selfLoc) <= 0 or isSelfMoved(lastLoc, selfLoc[0]):
                limitCount = 3
                break
            limitCount -= 1
            if len(selfLoc) > 0:
                print("self found")
                selfLoc = selfLoc[-1]
            else:
                print("self not found")
                inputhelper.dragRandom()
                enemyLoc = None
                time.sleep(2)
                break
            global minDistance
            distH = (selfLoc[0] - enemyLoc[0])
            distV = (selfLoc[1] - enemyLoc[1])
            if distH * distH + distV * distV >= minDistance * minDistance:
                distH = distH / 2
                distV = distV / 2
            if limitCount == 0 or distH * distH + distV * distV < 100 * 100:
                # enemyLoc = None
                # break
                if len(locs) == 1:
                    # clickBotton("withdraw")
                    # return None
                    inputhelper.dragRandom()
                    enemyLoc = None
                    break
                else:
                    locs.remove(enemyLoc)
                    enemyLoc = locs[-1]
                    break
            print("limitMove self: " + str(selfLoc) + ", dist "+ str(distH) +", " + str(distV) + ", loc "+ str(enemyLoc))
            clickToFight2([selfLoc[0] - distH , selfLoc[1] - distV], offset, size)
            lastLoc = selfLoc
            time.sleep(5)
            sourceImg = getScreenshot()
            
    return None


def formation(locations, sourceImg, subchapterName):
    locations = locations[0][0]
    print(locations)
    click(locations[0]+10, locations[1]+10, 200, 60, 80)
    time.sleep(2)

    bb = Configure.getScenes()["formation"].templates[0]
    hasItem, aa = matchTemplate.hasItem(sourceImg, cv.imread(bb.path), bb.threshold)
    if not hasItem:   
        time.sleep(10)
        return 'battleend'
    else:
        return 'formation'

def victory(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(5)
    return 'subchapter'


def getitem(locations, sourceImg, subchapterName):
    global lastScene
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(3)
    if lastScene == 'disbandY':
        return 'sellweapon'
    elif lastScene == 'aftersale':
        return 'disband'
    elif lastScene == 'battleend':
        return 'victory'
    elif lastScene == 'neterror':
        return 'sellweapon'
    return None


def getship(locations, sourceImg, subchapterName):
    click(locations[0][0][0] - 200, locations[0][0][1] - 200, 100, 50, 70)
    time.sleep(2)
    return 'getitem'


def battleend(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(1)
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(2)
    return 'getitem'

def avoid(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(2)
    return 'subchapter'

def full(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(2)
    return 'disband'

def clickSceneTemplate(locations, sourceImg, subchapterName):
    click(locations[0][0][0], locations[0][0][1], 100, 50, 70)
    time.sleep(2)
    return

def clickYes(locations, sourceImg, subchapterName):
    btn = Configure.getButton("yes")
    hasItem, loc = matchTemplate.hasItem(sourceImg, cv.imread(btn.path), btn.threshold)
    if hasItem:
        click(x=loc[0][0], y=loc[0][1], w=50, h=50, deltaT=50)
    time.sleep(2)
    return

def clickCancel(locations, sourceImg, subchapterName):
    btn = Configure.getButton("cancel")
    hasItem, loc = matchTemplate.hasItem(sourceImg, cv.imread(btn.path), btn.threshold)
    if hasItem:
        click(x=loc[0][0], y=loc[0][1], w=50, h=50, deltaT=50)
    time.sleep(2)
    return

def sellweapon(locations, sourceImg, subchapterName):
    clickYes(locations, sourceImg, subchapterName)
    clickCancel(locations, sourceImg, subchapterName)
    return 'getitem'

def ok(locations, sourceImg, subchapterName):
    global lastScene
    loc = locations[0][0]
    locations[0][0] = (loc[0] + 140, loc[1] + 10)
    clickSceneTemplate(locations, sourceImg, subchapterName)
    return lastScene

needDisBand = True
def disband(locations, sourceImg, subchapterName):
    global needDisBand
    if needDisBand:
        clickSceneTemplate(locations, sourceImg, subchapterName)
        return 'disbandY'
    else:
        clickCancel(locations, sourceImg, subchapterName)
        sourceImg = getScreenshot()
        disbandLabel = Configure.getScenes()['disband'].templates[0]
        hasItem, loc = matchTemplate.hasItem(sourceImg, cv.imread(disbandLabel.path), disbandLabel.threshold)
        if not hasItem:
            needDisBand = True
        return None

def disbandY(locations, sourceImg, subchapterName):
    global needDisBand
    clickYes(locations, sourceImg, subchapterName)
    needDisBand = False
    return 'getitem'

def sellweapon(locations, sourceImg, subchapterName):
    clickYes(locations, sourceImg, subchapterName)
    return 'aftersale'

def neterror(locations, sourceImg, subchapterName):
    global lastScene
    clickYes(locations, sourceImg, subchapterName)
    if lastScene == 'disbandY':
        return 'getitem'
    return lastScene

def aftersale(locations, sourceImg, subchapterName):
    clickYes(locations, sourceImg, subchapterName)
    return 'getitem'

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
    #船坞已满
    'full':         full,
    #退役
    'disband':      disband,
    #确定退役
    'disbandY':     disbandY,
    #拆解武器
    'sellweapon':   sellweapon,
    #“编队”页面，点击进入“战斗”页
    'formation':    formation,
    'victory':      victory,
    #点击继续
    'getitem':      getitem,
    'getship':      getship,
    #战斗评价页
    'battleend':    battleend,
    'ok':           ok,
    'neterror':     neterror,
    'aftersale':    aftersale
}


def splitSubchapterName(subchapterName):
    s, e = splitSubchapter(subchapterName)
    return s, e


def splitSubchapter(subchapterName):
    return subchapterName.split('-')


def battle(subchapterName, preferSenceIndex=0):
    preferStartLabel = None
    while True:
        sourceImg = getScreenshot()
        scence, locations = scencehelper.witchScence(sourceImg, preferSenceIndex, preferStartLabel)
        if scence:
            print(scence)
            lastScene = scence
            preferStartLabel = actionFunctions[scence](locations, sourceImg, subchapterName)
        else:  # error, try again
            time.sleep(3)

device = None
limitMove = False
lastScene = None
fleet = 1
fieldRect = Rect(180, 100, 1570, 850)
screenSize = 1080

def main(argv):
    global device
    global limitMove
    global fleet
    opts, args = getopt.getopt(argv, "c:d:l:p:f:", ["chapter=", "device=", "limie=", "profile=", "fleet="])
    subchapterName = None
    Configure.setResRootDir("./res/1080p_ch")
    for opt, arg in opts:
        if opt in ("-c", "--chapter"):
            subchapterName = arg
        elif opt in ("-d", "--device"):
            device = arg
            print("device "+str(device))
        elif opt in ("-l", "--limit"):
            limitMove = (arg == "True")
            print("device "+str(device))
        elif opt in ("-p", "--profile"):
            print("profile "+str(arg))
            Configure.setResRootDir(arg)
        elif opt in ("-f", "--fleet"):
            print("fleet "+str(arg))
            fleet = int(arg)
    # print(isSubchapterScene())
    getpic.screenshotStart(device)
    battle(subchapterName)

if __name__ == '__main__':
    main(sys.argv[1:])
