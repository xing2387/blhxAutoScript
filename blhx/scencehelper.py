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

def witchScence():
    outputFile = "lalala.jpg"
    getpic.downloadScreenshot(outputFile)
    for scence in Configure.getScenes():
        found = len(scence.templates) > 0
        for template in scence.templates:
            sourceImg = cv.imread(outputFile)
            templateImg = cv.imread(template.path)
            # showimg(sourceImg)
            # showimg(templateImg)
            if not matchTemplate.hasItem(sourceImg, templateImg, scence.threshold):
                found = False
                break
        if found:
            return scence.name



if __name__ == "__main__":
    getpic.screenshotStart()
    print(witchScence())