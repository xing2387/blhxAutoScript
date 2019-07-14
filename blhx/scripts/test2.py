#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import cv2 as cv
import numpy as np
# 画图的模块
import matplotlib.pyplot as plt

import getpic

def showimg(img):
    cv.imshow("image1", img)
    cv.waitKey(0)
    cv.destroyAllWindows()



##### 透视变换
filename = "/tmp/sdafwer.jpg"
getpic.downloadScreenshot(filename)
img = cv.imread(filename, 1)

imgW = img.shape[1]
imgH = img.shape[0]
insertWidth = imgH * 353 / 1080

m1 = np.float32(
    [[insertWidth, 0], [imgW - insertWidth, 0], [0, imgH], [imgW, imgH]])
m2 = np.float32([[0, 0], [imgW, 0], [0, imgH], [imgW, imgH]])

M = cv.getPerspectiveTransform(m1, m2)
dst = cv.warpPerspective(img, M, (imgW, imgH), cv.INTER_LINEAR)

showimg(dst)
##################
