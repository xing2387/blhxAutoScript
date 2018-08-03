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
    x = x + w * random.random()
    y = y + h * random.random()
    inputhelper.click(x, y, round(deltaT*random.random()))


def showimg(img):
    cv.imshow("image1", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def getScreenshot():
    getpic.downloadScreenshot("/tmp/sdafwer.jpg")
    return cv.imread("/tmp/sdafwer.jpg")

def home():
    None

def explore():
    None

actionFunctions = {
    'home':         home,
    'explore':    explore
}

def witchScence(scenes, sourceImg, preferStartIndex=0):
    if preferStartIndex >= len(scenes):
        return "halt" #返回一个不存在的场景让它报错
    
    fistIndex = preferStartIndex - len(scenes)
    for scence in scenes:
        points = []
        found = len(scence.templates) > 0
        for template in scence.templates:
            templateImg = cv.imread(template.path)
            # showimg(sourceImg)
            # showimg(templateImg)
            found, result = matchTemplate.hasItem(
                sourceImg, templateImg, template.threshold)
            if found:
                points.append(result)
            else:
                break
        if found:
            return scence.name, points
    return None, None


def battle(chapter):
    # while(True):
    None

def main(argv):
    # getpic.rootScreenshotStart()
    img = getScreenshot()
    templateImg = cv.imread("res_yys/chapter/c18.jpg")
    rec = matchTemplate.matchSingleTemplate(img, templateImg, 0.9)[0]
    size = templateImg.shape[:2]
    click(rec[0], rec[1], size[1], size[0], 50)
    print(rec)
    # showimg(img)
    opts, args = getopt.getopt(argv, "c:", ["chapter="])
    for opt, arg in opts:
        if opt in ("-c", "--chapter"):
            battle(arg)


if __name__ == '__main__':
    main(sys.argv[1:])
