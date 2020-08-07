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

def getAdbCommend(device):
    if not device:
        return "adb "
    else:
        return "adb -s " + device + " "

def screenshotStart(device=None):
    print("screenshotStart ")
    adb = getAdbCommend(device)
    if checkProcessExist(device):
        return
    os.system(adb + ' forward tcp:50087 tcp:50087')
    os.system(adb + ' forward tcp:50088 tcp:50088')
    os.system(
        adb + " shell 'x=/sdcard/Android/data/xxx.xxx.screenshotapp; if [[ ! -e $x ]] then mkdir $x;fi'"
    )
    os.system(
        adb + ' push classes.dex /sdcard/Android/data/xxx.xxx.screenshotapp/')
    os.system(
        adb + ''' shell 'x=/sdcard/Android/data/xxx.xxx.screenshotapp; 
            export CLASSPATH=$x/classes.dex; 
            exec app_process $x xxx.xxx.screenshotapp.MainControl'  &
        ''')
    os.system(
        adb + ''' shell 'x=/sdcard/Android/data/xxx.xxx.screenshotapp; 
            export CLASSPATH=$x/classes.dex; 
            exec app_process $x xxx.xxx.screenshotapp.MainScreenShot'  &
        ''')
    time.sleep(3)   #wait for the service start
    Started.setStarted(True)

def rootScreenshotStart(device=None):
    print("screenshotStart ")
    if checkProcessExist(device):
        return
    os.system('adb forward tcp:50087 tcp:50087')
    os.system('adb forward tcp:50088 tcp:50088')
    os.system(
        '''
        adb shell 'x=/data/app/$(su -c "ls /data/app|grep xxx.screenshotapp");
            if [[ -d $x ]] then
                export CLASSPATH=$x/base.apk;
            else 
                export CLASSPATH=$x;
            fi;
            exec app_process /system/bin xxx.xxx.screenshotapp.MainScreenShot &
            exec app_process /system/bin xxx.xxx.screenshotapp.MainControl & ' &
        '''
    )
    time.sleep(3)   #wait for the service start
    Started.setStarted(True)


def checkProcessExist(device=None):
    adb = getAdbCommend(device)
    result = os.popen(adb + ' shell "netstat -tnl | grep 5008"')
    started = "5008" in result.read()
    Started.setStarted(started)
    print("checkProcessExist: " + str(started))
    return Started.isStarted()


def checkStarted(tag=""):
    if not Started.isStarted() and not checkProcessExist():
        print(tag + " error! screenshot process is not started")
    return Started.isStarted()


def screenshotStop(device=None):
    print("screenshotStop ")
    if checkProcessExist(device):
        os.system(
            '''adb shell "netstat -tunlp 2>/dev/null |grep 50087 | awk '{print \$NF}' | cut -d / -f 1 | xargs kill -9"'''
        )
        os.system(
            '''adb shell "netstat -tunlp 2>/dev/null |grep 50088 | awk '{print \$NF}' | cut -d / -f 1 | xargs kill -9"'''
        )

def screenshotStop2(device=None):
    print("screenshotStop2 ")
    if checkProcessExist(device):
        os.system(
            '''adb shell "ps |grep app_process | awk '{print \$2}' | xargs kill -9"'''
        )
        os.system(
            '''adb shell "ps |grep app_process | awk '{print \$2}' | xargs kill -9"'''
        )

def downloadScreenshot(outputFilename, device=None):
    print("downloadScreenshot ")
    if checkProcessExist(device):
        req = requests.get('http://127.0.0.1:50087/screenshot?format="jpg"')
        with open(outputFilename, "wb") as outFile:
            outFile.write(req.content)


if __name__ == "__main__":
    action = sys.argv[1]
    if len(sys.argv) == 2:
        sys.argv.append(None)
    if "start" == action:
        screenshotStart(sys.argv[2])
    elif "root" == action:
        rootScreenshotStart(sys.argv[2])
    elif "stop" == action:
        screenshotStop(sys.argv[2])
    elif "stop2" == action:
        screenshotStop(sys.argv[2])
    elif "check" == action:
        checkProcessExist(sys.argv[2])
    elif "shot" == action:
        downloadScreenshot(sys.argv[2])
    # checkProcessExist()
    # screenshotStart()
    # downloadScreenshot("/tmp/sss.jpg")
    # screenshotStop()