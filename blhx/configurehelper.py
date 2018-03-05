#! /usr/bin/env python3

from __future__ import print_function
import json

'''
- base_dir:
    - st for scenseTemplates
    - eilb for enemy_icons-light_blue
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
    __subchapters = None
    __enemyIconsList = None

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
                    Scene(scence["name"], scence["templates"], scence["threshold"]))
        return cls.__scenes

    @classmethod
    def getSubchapters(cls):
        if not cls.__subchapters:
            print("init __subchapters")
            cls.__subchapters = cls.getConf()["subchapters"]
        return cls.__subchapters

    @classmethod
    def getEnemyIconsList(cls):
        if not cls.__enemyIconsList:
            print("init __enemyIconsList")
            enemyIconsList = {}
            for skey, svalue in cls.getSubchapters().items():
                # svalue是 {"e4":{}}
                enemyIconsList[skey] = {}
                for ekey, evalue in svalue.items():
                    # evalue是{"enemy_icons": []}
                    if a.has_key('enemy_icons'):
                        enemyIcons = []
                        icons = evalue["enemy_icons"]
                        for icon in icons:
                            enemyIcons.append(getPath(icon))
                        enemyIconsList[skey][ekey] = enemyIcons
            cls.__enemyIconsList = enemyIconsList
        return cls.__enemyIconsList

    @classmethod
    def getEnemyIcons(cls, chapter, subChapter):
        enemyIconsList = cls.getEnemyIconsList()
        return enemyIconsList[chapter][subChapter]


class Scene():
    __slots__ = "name", "threshold", "templates"

    def __init__(self, name, templates, threshold):
        '''  templates is a jsonArray '''
        self.name = name
        self.threshold = threshold
        self.templates = []
        for t in templates:
            self.templates.append(Template(t["path"], t["rect"]))


class Template():
    __slots__ = "path", "rect"

    def __init__(self, path, rect):
        self.rect = Rect(rect[0], rect[1], rect[2], rect[3])
        self.path = getPath(path)
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
