#! /usr/bin/env python3

from __future__ import print_function
import os
import requests
import time
import sys


class Started():
    __started = False

    @classmethod
    def isStarted(cls):
        # print("Started: " + str(cls.__started))
        return cls.__started

    @classmethod
    def setStarted(cls, started):
        cls.__started = started


def screenshotStart():
    print("screenshotStart ")
    if checkProcessExist():
        return
    os.system('adb forward tcp:53516 tcp:53516')
    os.system(
        "adb shell 'x=/sdcard/Android/data/xxx.xxx.screenshotapp; if [[ ! -e $x ]] then mkdir $x;fi'"
    )
    os.system(
        'adb push classes.dex /sdcard/Android/data/xxx.xxx.screenshotapp/')
    os.system(
        '''
        adb shell 'x=/sdcard/Android/data/xxx.xxx.screenshotapp; 
            export CLASSPATH=$x/classes.dex; 
            exec app_process $x xxx.xxx.screenshotapp.Main' >/dev/null &
        '''
    )
    time.sleep(3)   #wait for the service start
    Started.setStarted(True)

def rootScreenshotStart():
    print("screenshotStart ")
    if checkProcessExist():
        return
    os.system('adb forward tcp:53516 tcp:53516')
    os.system(
        '''
        adb shell 'x=/data/app/$(su -c ls /data/app|grep xxx.screenshotapp);
            if [[ -d $x ]] then
                export CLASSPATH=$x/base.apk;
            else 
                export CLASSPATH=$x; 
            fi;
            exec app_process /system/bin xxx.xxx.screenshotapp.Main' &
        '''
    )
    time.sleep(3)   #wait for the service start
    Started.setStarted(True)


def checkProcessExist():
    result = os.system('adb shell "netstat -tnl | grep 53516"')
    Started.setStarted(result == 0)
    print("checkProcessExist: " + str(result == 0))
    return Started.isStarted()


def checkStarted(tag=""):
    if not Started.isStarted() and not checkProcessExist():
        print(tag + " error! screenshot process is not started")
    return Started.isStarted()


def screenshotStop():
    print("screenshotStop ")
    if checkStarted("screenshotStop"):
        os.system(
            '''adb shell "netstat -tunlp 2>/dev/null |grep 53516 | awk '{print \$NF}' | cut -d / -f 1 | xargs kill -9"'''
        )
    time.sleep(3)   #wait for the service stop


def downloadScreenshot(outputFilename):
    print("downloadScreenshot ")
    if checkStarted("downloadScreenshot"):
        req = requests.get('http://127.0.0.1:53516/screenshot.jpg')
        with open(outputFilename, "wb") as outFile:
            outFile.write(req.content)


if __name__ == "__main__":
    action = sys.argv[1]
    if "start" == action:
        screenshotStart()
    elif "root" == action:
        rootScreenshotStart()
    elif "stop" == action:
        screenshotStop()
    elif "check" == action:
        checkProcessExist()
    elif "shot" == action:
        downloadScreenshot(sys.argv[2])
    # checkProcessExist()
    # screenshotStart()
    # downloadScreenshot("/tmp/sss.jpg")
    # screenshotStop()