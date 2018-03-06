#! /usr/bin/env python3

from __future__ import print_function
import json

'''
- base_dir:
    - st    for scenseTemplates
    - eilb  for enemy_icons-light_blue
    - scl   for subchapter labels
- scenes:
    - sences: [main, precombat, subchapter]
    - templates:
        - rect: [x, y, w, h]
'''


def getPath(path):
    prefix, path = path.split("#")
    return Configure.getBaseDir()[prefix] + path


class Configure():
    __configure = None
    __baseDir = None
    __scenes = None
    __enemyIconsList = None
    __chapterLabels = None
    __subchapterLabels = None
    __chapters = None

    @classmethod
    def getConf(cls):
        if not cls.__configure:
            print("init __configure")
            f = open("configure.json", encoding='utf-8')
            cls.__configure = json.load(f)
        return cls.__configure

    @classmethod
    def getBaseDir(cls):
        if not cls.__baseDir:
            print("init __baseDir")
            cls.__baseDir = cls.getConf()["base_dir"]
        return cls.__baseDir

    @classmethod
    def getScenes(cls):
        if not cls.__scenes:
            print("init __scenes")
            scenes = cls.getConf()["scenes"]
            cls.__scenes = []
            for scence in scenes:
                cls.__scenes.append(
                    Scene(scence["name"], scence["templates"]))
        return cls.__scenes

    @classmethod
    def __parseSubchaptersConfig(cls):
        if not cls.__enemyIconsList:
            print("init __enemyIconsList")
            enemyIconsList = {}
            chapterLabels = {}
            subchapterLabels = {}
            chapters = {}
            for skey, svalue in cls.getConf()["chapters"].items():
                # svalue是 {"templates":[], "e4":{}}
                for ekey, evalue in svalue.items():
                    if "enemy_icons" in evalue.keys():
                        # evalue是{"templates":[], "enemy_icons": []}
                        enemyIconsList[skey] = {}
                        enemyIcons = []
                        subchapterLabels[skey] = {}
                        for icon in evalue["enemy_icons"]:
                            enemyIcons.append(getPath(icon))
                        for label in evalue["templates"]:
                            if "elabel" == label["name"]:
                                subchapterLabels[skey][ekey] = Template(
                                    getPath(label["path"]), label["rect"], label["name"], label["threshold"])
                        enemyIconsList[skey][ekey] = enemyIcons
                    elif "templates" == ekey:
                        for label in evalue:
                            if "slabel" == label["name"]:
                                chapterLabels[skey] = Template(
                                    getPath(label["path"]), label["rect"], label["name"], label["threshold"])
                chapters[skey] = Chapter(skey, svalue[])
            cls.__chapterLabels = chapterLabels
            cls.__subchapterLabels = subchapterLabels
            cls.__enemyIconsList = enemyIconsList
            cls.__chapters = chapters

    @classmethod
    def getEnemyIcons(cls, chapter, subChapter):
        if not cls.__enemyIconsList:
            cls.__parseSubchaptersConfig()
        return cls.__enemyIconsList[chapter][subChapter]

    @classmethod
    def getSubchapterLabels(cls, chapter):
        if not cls.__subchapterLabels:
            cls.__parseSubchaptersConfig()
        return cls.__subchapterLabels

    @classmethod
    def getChapterLabels(cls):
        if not cls.__chapterLabels:
            cls.__parseSubchaptersConfig()
        return cls.__chapterLabels


class Subchapter():
    __slots__ = "name", "labels", "enemyIcons"

    def __init__(self, name, labels, enemyIcons):
        ''' subchapters,labels is an Object List '''
        self.name = name
        self.labels = labels
        self.enemyIcons = enemyIcons


class Chapter():
    __slots__ = "name", "pageIndex", "labels", "subchapters"

    def __init__(self, name, pageIndex, labels, subchapters):
        ''' subchapters,labels is an Object List '''
        self.name = name
        self.pageIndex = pageIndex
        self.labels = labels
        self.subchapters = subchapters


class Scene():
    __slots__ = "name", "templates"

    def __init__(self, name, templates):
        '''  templates is a jsonArray '''
        self.name = name
        self.templates = []
        for t in templates:
            self.templates.append(
                Template(t["path"], t["rect"], t["name"], t["threshold"]))


class Template():
    __slots__ = "path", "rect", "name", "threshold"

    def __init__(self, path, rect, name, threshold):
        self.rect = Rect(rect[0], rect[1], rect[2], rect[3])
        self.path = getPath(path)
        self.name = name
        self.threshold = threshold
        # prefix, path = path.split("#")
        # self.path = Configure.getBaseDir()[prefix] + path


class Rect():
    __slots__ = "x", "y"
    __slots__ += "width", "height"

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


if __name__ == "__main__":
    print(Configure.getScenes())
    print(Configure.getScenes()[0].templates[0].path)
    print(Configure.getEnemyIcons('s3', 'e4'))
    # print(getScene().name)
