#! /usr/bin/env python3

from __future__ import print_function
import numpy as np
import time
import threading
import getpic
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
        if abs(pt[0] - x1) > width or abs(pt[1] - y1) > height:
            result.append(pt)
            x1 = pt[0]
            y1 = pt[1]
    return result


def hasItem(sourceImg, templateImg, threshold, mask=None, mark=False):
    result = matchSingleTemplate(sourceImg, templateImg, threshold, mask, mark)
    print(result)
    return len(result) > 0, result


def hasItemInRect(sourceImg, templateImg, threshold, rect, mask=None, mark=False):
    loc = matchSingleTemplateInRect(sourceImg, templateImg, threshold, rect, mask, mark)
    print(loc)
    return len(loc) > 0, loc


def matchSingleTemplateInRect(sourceImg, templateImg, threshold, rect, mask=None, mark=False):
    ''' Args:
            rect: Object of class Rect with '__slots__ = "x", "y", "width", "height"'
    '''
    sourceImg = sourceImg[rect.y:rect.y + rect.height, rect.x:rect.x + rect.width]
    # showimg(sourceImg)
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
    res = cv.matchTemplate(sourceImg, templateImg, cv.TM_CCOEFF_NORMED, mask = mask)

    loc = np.where(res >= threshold)
    foundPoints = filterPoints(zip(*loc[::-1]), w, h)
    result = []
    logs = []
    for pt in foundPoints:
        result.append([pt[0], pt[1]])
        logs.append((pt[0], pt[1], res[pt[1]][pt[0]]))
        if mark:
            cv.rectangle(sourceImg, (pt[0], pt[1]),
                        (pt[0] + w, pt[1] + h), (255, 249, 151), 2)
    print(logs)
    if mark:
        showimg(sourceImg)
    return result


def matchMutiTemplateInRect(sourceImg, templateImgs, threshold, rect=None, outFilename=None, masks=None, mark=False):
    if rect:
        sourceImg = sourceImg[rect.y:rect.y + rect.height, rect.x:rect.x + rect.width]
    # showimg(sourceImg)
    result = matchMutiTemplate(sourceImg, templateImgs, threshold, outFilename, masks, mark)
    if len(result) > 0:
        for aa in result:
            aa[0] += rect.x
            aa[1] += rect.y
    return result


def matchMutiTemplate(sourceImg, templateImgs, threshold, outFilename=None, masks=None, mark=False):
    # threads = []
    h, w = templateImgs[0].shape[:2]
    for templateImg in templateImgs:
        h0, w0 = templateImg.shape[:2]
        if h0 < h:
            h = h0
        if w0 < w:
            w = w0
    pointsList = []
    with Pool(5) as p:
        for i in range(0, len(templateImgs)):
            # print("--------- " + str(i))
            mask = None
            if masks:
                mask =  masks[i]
            pointsList.append(p.apply(matchSingleTemplate, kwds={'sourceImg': sourceImg, 'templateImg': templateImgs[i], 'threshold': threshold}))
    points = []
    for pts in pointsList:
        for pt in pts:
            points.append([pt[0], pt[1]])
    points.sort(key=lambda x: [x[0], x[1]])
    print("~~~~~~~~~~~~~~~~~~~matchMutiTemplate " + str(points))
    result = filterPoints(points, w, h)
    if outFilename:
        cv.imwrite(outFilename, sourceImg)
    return result


if __name__ == "__main__":
    base_dir = "./"
    # dir_out = base_dir + "out/"
    # dir_src = base_dir + "src/"
    # files_source = []
    # files_template = []
    # for x in range(1, 15):
    #     files_source.append(dir_src + str(x) + '.png')
    # # files_template.append(dir_src + 't3.png')
    # files_template.append(dir_src + 't6.png')
    # # files_template.append(dir_src + 't5.png')
    # # files_template.append(dir_src + 'my.jpg')
    # # maskImg = None
    # maskImg = cv.imread(dir_src + "t7.png")
    # templateImgs = []
    # for x in files_template:
    #     templateImgs.append(cv.imread(x))

    # tStart = time.time()
    # print(matchMutiTemplate(
    #     cv.imread(files_source[8]), templateImgs, 0.4, mask=maskImg))
    # # for xx in files_source:
    # #     print(matchMutiTemplate(cv.imread(xx), templateImgs, 0.4, mask=maskImg))
    # print("totel time used: " + str(time.time() - tStart))
    devices = "cb5621bf"
    getpic.downloadScreenshot("/tmp/sss.jpg", devices)
    img = cv.imread("/tmp/sss.jpg")
    # showimg(img)
    # img = cv.imread(base_dir+"/image1_screenshot_13.07.2019.png")

    # imgW = img.shape[1]
    # imgH = img.shape[0]
    # insertWidth = imgH * 310 / 1080

    # m1 = np.float32(
    #     [[insertWidth, 0], [imgW - insertWidth, 0], [0, imgH], [imgW, imgH]])
    # m2 = np.float32([[0, 0], [imgW, 0], [0, imgH], [imgW, imgH]])

    # M = cv.getPerspectiveTransform(m1, m2)
    # dst = cv.warpPerspective(img, M, (imgW, imgH), cv.INTER_LINEAR)x-special/nautilus-clipboard
    # showimg(dst)x-special/nautilus-clipboardx-special/nautilus-clipboardx-special/nautilus-clipboardx-special/nautilus-clipboardx-special/nautilus-clipboard

    template = cv.imread("/Users/xing/workspace/myself/blhxAutoScript/blhx/scripts/res/1080p_ch/buttons/notreach.png")
    mask = cv.imread("/home/xing/workspace/myself/blhxAutoScript/blhx/scripts/res/enemy_icons/mask2.png")
    result = matchSingleTemplate(img, template, 0.8, None, False)
    # print(result)

    # h=[140, 150]
    # s=[102, 127]
    # v=[114, 250]
    # imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # hsvSplit = cv.split(imgHSV)
    # hsvSplit[2] = cv.equalizeHist(hsvSplit[2])
    # imgHSV = cv.merge(hsvSplit, imgHSV)
    # print(imgHSV)
    # showimg(img)