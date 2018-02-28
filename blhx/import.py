#! /usr/bin/env python

from __future__ import print_function
import code
import numpy as np
import cv2 as cv
import functools
from multiprocessing import Pool

src = "test/src/9.png"
templ = "test/src/t6.png"
srcImg = cv.imread(src, cv.IMREAD_GRAYSCALE)
templImg = cv.imread(templ)

def showimg(img):
    cv.imshow("image1", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

aa, threImg = cv.threshold(srcImg, 80, 255, cv.THRESH_BINARY)
# showimg(threImg)
image, contours, hierarchy = cv.findContours(threImg, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

h, w = image.shape[:2]
vis = np.zeros((h, w, 3), np.uint8)
contours0 = contours#[cv.approxPolyDP(cnt, 3, True) for cnt in contours]
aaa = cv.drawContours(vis, contours0, -1, (128,255,255), 3, cv.LINE_AA, hierarchy, 1)
showimg(aaa)
# cv.imwrite('test/src/my.jpg', threImg)

# code.interact(banner="",local=locals())

