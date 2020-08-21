#! /usr/bin/env python3

from __future__ import print_function
from configurehelper import Configure
import getpic
import matchTemplate
import cv2 as cv


def showimg(img):
    cv.imshow("image1", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def witchScence(sourceImg, preferStartIndex=0, preferStartLabel=None):
    count = len(Configure.getScenes().values())
    if preferStartLabel:
        for x in range(count):
            if list(Configure.getScenes().values())[x].name == preferStartLabel:
                preferStartIndex = x

    if preferStartIndex >= count:
        return "halt" #返回一个不存在的场景让它报错
    
    fistIndex = preferStartIndex - count
    origList = list(Configure.getScenes().values())
    scenes = []
    for x in range(fistIndex, preferStartIndex):
        scenes.append(origList[x])
    for scence in scenes:
        points = []
        found = len(scence.templates) > 0
        for template in scence.templates:
            print(template.path)
            # showimg(sourceImg)
            # showimg(templateImg)
            found, result = matchTemplate.hasItem(sourceImg, template.getImg(), template.threshold)
            if found:
                points.append(result)
            else:
                break
        if found:
            return scence.name, points
    return None, None


if __name__ == "__main__":
    getpic.screenshotStart()
    print(witchScence())
