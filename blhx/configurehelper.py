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
    __buttons = None

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
    def getChapters(cls):
        if not cls.__chapters:
            print("init __chapters")
            cls.__chapters = {}
            chapters = cls.getConf()["chapters"]
            for chapter in chapters:
                cls.__chapters[chapter["name"]
                               ] = Chapter.parseFromDict(chapter)
        return cls.__chapters

    @classmethod
    def getButtons(cls):
        if not cls.__buttons:
            print("init __buttons")
            cls.__buttons = {}
            buttons = cls.getConf()["buttons"]
            for button in buttons:
                cls.__buttons[button["name"]] = Template.parseFromDict(button)
        return cls.__buttons

    @classmethod
    def getButton(cls, name):
        return cls.getButtons()[name]

    @classmethod
    def getChapter(cls, chapter):
        return cls.getChapters()[chapter]

    @classmethod
    def getSubchapter(cls, chapter, subchapter):
        return cls.getChapters()[chapter].subchapters[subchapter]

    @classmethod
    def getEnemyIcons(cls, chapter, subChapter):
        return cls.getSubchapter(chapter, subChapter).enemyIcons

    @classmethod
    def getSubchapterLabel(cls, chapter, subChapter):
        return cls.getSubchapter(chapter, subChapter).label


class Subchapter():
    __slots__ = "name", "labels", "enemyIcons", "bossDirect", "fight"
    ''' bossDirect, start from left top corner, clockwise [0,1,2,3,4,5,6,7,8], -1 for any where'''
    ''' fight for "how many fight before meeting boss" '''
    @classmethod
    def parseFromDict(cls, dataDict):
        subchapter = dataDict
        name = subchapter["name"]
        bossDirect = subchapter["boss_direct"]
        fight = subchapter["fight"]
        labels = []
        for label in subchapter["templates"]["elabel"]:
            labels.append(Template.parseFromDict(label))
        enemyIcons = []
        for enemyIcon in subchapter["enemy_icons"]:
            enemyIcons.append(getPath(enemyIcon))
        return Subchapter(name, labels, enemyIcons, bossDirect, fight)

    def __init__(self, name, labels, enemyIcons, bossDirect, fight):
        self.name = name
        self.labels = labels
        self.enemyIcons = enemyIcons
        self.bossDirect = bossDirect
        self.fight = fight


class Chapter():
    __slots__ = "name", "pageIndex", "labels", "subchapters"

    @classmethod
    def parseFromDict(cls, dataDict):
        chapter = dataDict
        labels = []
        subchapters = {}
        for label in chapter["templates"]["slabel"]:
            labels.append(Template.parseFromDict(label))
        if not chapter["subchapters"]:
            for subchapter in chapter["subchapters"]:
                subchapters[subchapter["name"]
                            ] = Subchapter.parseFromDict(subchapter)
        name = chapter["name"]
        pageIndex = chapter["pageIndex"]
        return Chapter(name, pageIndex, labels, subchapters)

    def __init__(self, name, pageIndex, labels, subchapters):
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

    @classmethod
    def parseFromDict(cls, dataDict):
        return Template(dataDict["path"], dataDict["rect"], dataDict["name"], dataDict["threshold"])

    def __init__(self, path, rect, name, threshold):
        self.rect = Rect(rect[0], rect[1], rect[2], rect[3])
        self.path = getPath(path)
        self.name = name
        self.threshold = threshold


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
