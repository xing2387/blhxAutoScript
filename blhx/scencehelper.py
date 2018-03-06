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


def witchScence(sourceImg=None, preferStartIndex=0):
    count = len(Configure.getScenes())
    if preferStartIndex >= count:
        return "halt" #返回一个不存在的场景让它报错
    if not sourceImg.any():
        getpic.downloadScreenshot("/tmp/sdafwer.jpg")
        sourceImg = cv.imread("/tmp/sdafwer.jpg")
    
    fistIndex = preferStartIndex - count
    scenes = []
    for x in range(fistIndex, preferStartIndex):
        print("witchScence, " + str(x))
        scenes.append(Configure.getScenes()[x])
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


if __name__ == "__main__":
    getpic.screenshotStart()
    print(witchScence())
