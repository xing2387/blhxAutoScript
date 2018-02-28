#! /usr/bin/env python

import cv2 as cv
import numpy as np
import code
import sys
sys.path.append('../')
import utils
import time
import threading
import functools


base_dir = "/home/xing/Desktop/aaa/"
dir_out = base_dir + "out/"
dir_src = base_dir + "src/"


files_source = []
for x in range(1,15):
    files_source.append(dir_src + str(x) + '.png')
files_template = []
files_template.append(dir_src + 't3.png')
files_template.append(dir_src + 't6.png')
files_template.append(dir_src + 't5.png')

def getFilename(fullFilename):
    return fullFilename[fullFilename.rfind('/') + 1 : fullFilename.rfind('.')]

def findImgSingleTemplate(sourceImg, templateImg, threshold):
#        templateImg = cv.imread(templateFile)
        w,h = templateImg.shape[0:2][::-1]
        res = cv.matchTemplate(sourceImg, templateImg, cv.TM_CCOEFF_NORMED)
#        utils.showimg(res)
        loc = np.where(res >= threshold)
        x1 = y1 = -10000
        for pt in zip(*loc[::-1]):
            if pt[0] > x1 + w or pt[1] > y1 + h:
                print pt
                #cv.rectangle(res, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (255,249,151), 2)
                cv.rectangle(sourceImg, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (255,249,151), 2)
                x1 = pt[0]
                y1 = pt[1]

def findImg(sourceImg, templateImgs, threshold, outFilename):
#    print "source file: " + sourceFile
#    sourceImg = cv.imread(sourceFile)
    timeStart = time.time()
    threads = []
    for templateImg in templateImgs:
        t = threading.Thread(target=functools.partial(findImgSingleTemplate, sourceImg, templateImg, threshold))
        t.start()
        threads.append(t)
    for tt in threads:
        tt.join()

#        findImgSingleTemplate(sourceImg, templateImg, threshold)
#    utils.showimg(img_source)
    print "use time: " + str(time.time() - timeStart) + "s"
#    outputFile = dir_out + getFilename(sourceFile) + \
#                    templateFile[templateFile.rfind('/') + 1 : ]
    print "saving file at: " + outFilename
    cv.imwrite(outFilename, sourceImg)

threshold = 0.4
tStart = time.time()
#findImg(dir_src + "13.png", files_template, threshold)
templateImgs = []
for x in files_template:
    templateImgs.append(cv.imread(x))
for x in files_source:
    outputFile = dir_out + getFilename(x) + ".png"
    sourceImg = cv.imread(x)
    findImg(sourceImg, templateImgs, threshold, outputFile)

#findImg(cv.imread(dir_src + "9.png"), templateImgs, threshold, dir_out + "9.png")
print "totel time used: " + str(time.time() - tStart)

#code.interact(banner="",local=locals())


