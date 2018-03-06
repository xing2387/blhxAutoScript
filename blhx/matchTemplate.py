#! /usr/bin/env python3

from __future__ import print_function
import numpy as np
import time
import threading
import functools
from multiprocessing import Pool
import cv2 as cv


def showimg(img):
    cv.imshow("image1", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def filterPoints(points, width, height):
    result = []
    x1 = y1 = -10000
    for pt in points:
        if pt[0] > x1 + width or pt[1] > y1 + height:
            result.append(pt)
            x1 = pt[0]
            y1 = pt[1]
    return result


def hasItem(sourceImg, templateImg, threshold, mask=None, mark=False):
    result = matchSingleTemplate(sourceImg, templateImg, threshold, mask, mark)
    print(result)
    return len(result) > 0, result

def hasItemInRect(sourceImg, templateImg, threshold, rect, mask=None, mark=False):
    result = matchSingleTemplateInRect(sourceImg, templateImg, threshold, rect, mask, mark)
    print(result)
    return len(result) > 0, result

def matchSingleTemplateInRect(sourceImg, templateImg, threshold, rect, mask=None, mark=False):
    sourceImg = sourceImg[rect.y:rect.y + rect.height, rect.x:rect.x + rect.width]
    showimg(sourceImg)
    result = matchSingleTemplate(sourceImg, templateImg, threshold, mask, mark)
    if len(result) > 0:
        aa = result[0]
        aa[0] += rect.x
        aa[1] += rect.y
    return result

def matchSingleTemplate(sourceImg, templateImg, threshold, mask=None, mark=False):
    """ looking for the position of the templateImg in the sourceImg
    Args:
        threshold: the threshold of TM_CCOEFF_NORMED, 
        mark:   whether draw ractangle in the sourceImg
    """
    h, w = templateImg.shape[:2]
    # aa, threImg = cv.threshold(sourceImg, 80, 255, cv.THRESH_BINARY)
    # res = cv.matchTemplate(threImg, templateImg, cv.TM_CCOEFF_NORMED, mask)
    res = cv.matchTemplate(sourceImg, templateImg, cv.TM_CCOEFF_NORMED)
    # if res.any():
    print("matchSingleTemplate, max value: " + str(np.max(res)))
    
    loc = np.where(res >= threshold)
    foundPoints = filterPoints(zip(*loc[::-1]), w, h)
    result = []
    for pt in foundPoints:
        result.append([pt[0] + w/2, pt[1] + h/2])
        print(res[int(pt[1]), pt[0]])
        if mark:
            print(pt)
            #cv.rectangle(res, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (255,249,151), 2)
            cv.rectangle(sourceImg, (pt[0], pt[1]),
                         (pt[0] + w, pt[1] + h), (255, 249, 151), 2)
    return result


def matchMutiTemplate(sourceImg, templateImgs, threshold, outFilename=None, mask=None, mark=False):
    # threads = []
    h, w = templateImgs[0].shape[:2]
    for templateImg in templateImgs:
        h0, w0 = templateImg.shape[:2]
        if h0 < h:
            h = h0
        if w0 < w:
            w = w0
    points = []
    with Pool(5) as p:
        func = functools.partial(
            matchSingleTemplate, sourceImg, threshold=threshold, mask=mask, mark=mark)
        points = p.map(func, templateImgs)
    result = filterPoints(points[0], w, h)
    if outFilename:
        cv.imwrite(outFilename, sourceImg)
    return result


if __name__ == "__main__":
    base_dir = "test/"
    dir_out = base_dir + "out/"
    dir_src = base_dir + "src/"
    files_source = []
    files_template = []
    for x in range(1, 15):
        files_source.append(dir_src + str(x) + '.png')
    # files_template.append(dir_src + 't3.png')
    files_template.append(dir_src + 't6.png')
    # files_template.append(dir_src + 't5.png')
    # files_template.append(dir_src + 'my.jpg')
    # maskImg = None
    maskImg = cv.imread(dir_src + "t7.png")
    templateImgs = []
    for x in files_template:
        templateImgs.append(cv.imread(x))

    tStart = time.time()
    print(matchMutiTemplate(
        cv.imread(files_source[8]), templateImgs, 0.4, mask=maskImg))
    # for xx in files_source:
    #     print(matchMutiTemplate(cv.imread(xx), templateImgs, 0.4, mask=maskImg))
    print("totel time used: " + str(time.time() - tStart))
