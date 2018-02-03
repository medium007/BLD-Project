import json
import heapq as hq
import random

from constants import *


class Dictionary:

    def __init__(self):
        self.queue = []

        try:
            f = open(PATH_TO_JSON, 'r', encoding='utf-8')
            self.dict = json.load(f)
            f.close()

        except FileNotFoundError:
            self.dict = None
            return

    def getCorners(self):
        return self.dict.get(CORNERS)

    def getWord(self, word):
        return self.getCorners().get(word)

    def getWordFromStickers(self, sticker1, sticker2):
        for word in self.getWordsList():
            if self.getSticker1(word) == sticker1 and self.getSticker2(word) == sticker2:
                return word
        return None

    def getAlg(self, word):
        return self.getCorners().get(word).get(ALG)

    def getType(self, word):
        return self.getWord(word).get(TYPE)

    def getSticker1(self, word):
        return self.getWord(word).get(STICKER1)

    def getSticker2(self, word):
        return self.getWord(word).get(STICKER2)

    def getChecked(self, word):
        return self.getWord(word).get(CHECKED)

    def getNoOfGoodAnswers(self, word):
        return self.getWord(word).get(GOOD_ANSWERS)

    def getNoOfBadAnswers(self, word):
        return self.getWord(word).get(BAD_ANSWERS)

    def getWordFromQueue(self):
        return self.queue.pop(0)[1]

    def getQueueLength(self):
        return len(self.queue)

    def getWordsList(self):
        return self.dict[CORNERS]

    def setAlg(self, word, alg):
        self.getWord(word).update({ALG: alg})

    def setSticker1(self, word, sticker):
        self. getWord(word).update({STICKER1: sticker})

    def setSticker2(self, word, sticker):
        self.getWord(word).update({STICKER2: sticker})

    def setChecked(self, word, toSet='yes'):
        self.getWord(word).update({CHECKED: toSet})

    def setNoOfGoodAnswers(self, word, n):
        self.getWord(word).update({GOOD_ANSWERS: n})

    def setNoOfBadAnswers(self, word, n):
        self.getWord(word).update({BAD_ANSWERS: n})

    def removeAlg(self, word):
        self.setAlg(word, '')

    def createCom(self, setup, alg1, alg2):
        com = ''

        if setup:
            com = '%s %s:' % (com, setup)

        if alg2:
            com = '%s [ %s, %s ]' % (com, alg1, alg2)
        else:
            com = '%s ( %s )' % (com, alg1)

        return com

    def createPriorityQueue(self, workingType):
        q = []
        for word in self.getWordsList():
            if TYPES[workingType] == ALL_TYPES or TYPES[workingType] == self.getType(word):
                g = self.getNoOfGoodAnswers(word)
                b = self.getNoOfBadAnswers(word)
                if g == 0 and b == 0:
                    priority = 0
                else:
                    priority = self.calculatePriority(g, b)
                hq.heappush(q, (priority, word))
    
        priority = 0
        tempQueue = []
        sortedQueue = []
        while len(q):
            item = hq.heappop(q)
            if priority == item[0]:
                tempQueue.append(item)
            else:
                priority = item[0]
                random.shuffle(tempQueue)
                sortedQueue += tempQueue
                tempQueue = [item]
    
        random.shuffle(tempQueue)
        sortedQueue += tempQueue
        self.queue = sortedQueue

    def calculatePriority(self, g, b):
        return g / (g + b)

    def addMirrorAlg(self, setup, alg1, alg2, sticker1, sticker2):
        if alg2:
            word = self.getWordFromStickers(sticker1, sticker2)
            comm = self.createCom(setup, alg2, alg1)
            self.setAlg(word, comm)
            return True
        else:
            return False

    def saveDict(self):
        f = open(PATH_TO_JSON, 'w', encoding='utf-8')
        json.dump(self.dict, f, indent=8, ensure_ascii=False)
        f.close()

    def sortWordsInDictionary(self):
        os.system('cls')
        newDct = {CORNERS: {}}
        for i in range(ord('A'), ord('Z') + 1):
            for j in range(ord('A'), ord('Z') + 1):
                for word in self.getWordsList():
                    if self.getSticker1(word) == chr(i) and self.getSticker2(word) == chr(j):
                        newDct.get(CORNERS).update({word: self.dict.get(CORNERS)[word]})
                        break
        self.dict = newDct
        self.saveDict()
