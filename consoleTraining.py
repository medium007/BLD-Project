import json
import heapq as hq
import random
from constants import *
import os


def loadJSON():
    try:
        f = open(PATH_TO_JSON, 'r', encoding='utf-8')
        dct = json.load(f)
        f.close()
        return dct
    except FileNotFoundError:

        input('File (%s) not found, press any key to exit' %PATH_TO_JSON)
        exit(1)


def train(dct):
    workingType = workWithType()
    queue = createPriorityQueue(dct, workingType)
    continueTraining = True

    while continueTraining:
        os.system('cls')
        priority, word = queue.pop(0)
        print('Word:\t%s' % word)
        yn = input('Do you know it? (y/n): ')

        if yn == 'y' or yn == '':
            goodAnswer(dct, word)
        elif yn == 'n':
            badAnswer(dct, word)
        else:
            continueTraining = False

        saveDict(dct, True)

        if len(queue) == 0:
            print('\nNo more left commutators.')
            yn = input('Do you want to continue? (y/n): ')
            if yn == 'y':
                queue = createPriorityQueue(dct, workingType)
            else:
                continueTraining = False

    saveDict(dct)


def addAlgs(dct):
    os.system('cls')
    for word in dct[CORNERS]:
        if not getAlg(dct, word):    # and getSticker1(word) in ['T', 'W', 'Z']:
            print('Word %s' % word)
            setup = input('Setup: ')
            if setup == 'exit':
                saveDict(dct)
                return
            alg1 = input('Alg1: ')
            alg2 = input('Alg2: ')

            setAlg(dct, word, createCom(setup, alg1, alg2))
            addMirrorAlg(dct, setup, alg1, alg2, getSticker2(dct, word), getSticker1(dct, word))
    print('All words have an alg')
    saveDict(dct)


def getCorners(dct):
    return dct.get(CORNERS)


def getWord(dct, word):
    return getCorners(dct).get(word)


def getAlg(dct, word):
    return dct.get(CORNERS).get(word).get(ALG)


def setAlg(dct, word, alg):
    getWord(dct, word).update({ALG: alg})


# deprecated
def getScore(dct, word):
    return getWord(dct, word).get('score')


# deprecated
def setScore(dct, word, n):
    getWord(dct, word).update({'score': n})


def saveAndExit(dct):
    saveDict(dct)
    exit(0)


def saveDict(dct, quiet=False):
    f = open(PATH_TO_JSON, 'w', encoding='utf-8')
    json.dump(dct, f, indent=8, ensure_ascii=False)
    f.close()
    if not quiet:
        print('\nDictionary saved!')
        input("Press Enter to continue...")


def workWithType():
    os.system('cls')
    print(WORKTYPE_MENU)
    workingType = int(input('> '))
    return workingType


def getType(dct, word):
    return getWord(dct, word).get(TYPE)


def createCom(setup, alg1, alg2):
    com = ''

    if setup:
        com = '%s %s:' % (com, setup)

    if alg2:
        com = '%s [ %s, %s ]' % (com, alg1, alg2)
    else:
        com = '%s ( %s )' % (com, alg1)

    return com


def getSticker1(dct, word):
    return getWord(dct, word).get(STICKER1)


def getSticker2(dct, word):
    return getWord(dct, word).get(STICKER2)


def setSticker1(dct, word, sticker):
    getWord(dct, word).update({STICKER1: sticker})


def setSticker2(dct, word, sticker):
    getWord(dct, word).update({STICKER2: sticker})


def addMirrorAlg(dct, setup, alg1, alg2, sticker1, sticker2):
    for word in dct[CORNERS]:
        if getSticker1(dct, word) == sticker1 and getSticker2(dct, word) == sticker2:
            if alg2:
                comm = createCom(setup, alg2, alg1)
                setAlg(dct, word, comm)
                print('Created mirror comm for %s : %s' % (word, comm))
                return
            else:
                print('Not created mirror comm for %s' % word)
                return


def isChecked(dct, word):
    return getWord(dct, word).get(CHECKED)


def checkAlgs(dct):
    os.system('cls')
    for word in dct[CORNERS]:
        if not isChecked(dct, word):
            print('\n%s: %s' % (word, getAlg(dct, word)))
            cmd = input('Is it correct?')
            if cmd == 'n' or cmd == 'N':
                removeAlg(dct, word)
                addAlgs(dct)
            elif cmd == 'e' or cmd == 'E':
                saveDict(dct)
                return
            else:
                setChecked(dct, word)

    print('All commutators are checked.')
    saveDict(dct)


def setChecked(dct, word, toSet='yes'):
    getWord(dct, word).update({CHECKED: toSet})


def removeAlg(dct, word):
    setAlg(dct, word, '')


def sortDict(dct):
    os.system('cls')
    newDct = {CORNERS: {}}
    for i in range(ord('A'), ord('Z') + 1):
        for j in range(ord('A'), ord('Z') + 1):
            for word in dct[CORNERS]:
                if getSticker1(dct, word) == chr(i) and getSticker2(dct, word) == chr(j):
                    newDct.get(CORNERS).update({word: dct.get(CORNERS)[word]})
                    # print(dct.get(CORNERS)[word])
                    break
    dct = newDct
    print('Dictionary sorted.')
    saveDict(dct)


def getNoOfGoodAnswers(dct, word):
    return getWord(dct, word).get(GOOD_ANSWERS)


def getNoOfBadAnswers(dct, word):
    return getWord(dct, word).get(BAD_ANSWERS)


def setNoOfGoodAnswers(dct, word, n):
    getWord(dct, word).update({GOOD_ANSWERS: n})


def setNoOfBadAnswers(dct, word, n):
    getWord(dct, word).update({BAD_ANSWERS: n})


def calculatePriority(g, b):
    return g / (g + b)


def createPriorityQueue(dct, workingType):
    queue = []
    for word in dct[CORNERS]:
        if TYPES[workingType] == ALL_TYPES or TYPES[workingType] == getType(dct, word):
            g = getNoOfGoodAnswers(dct, word)
            b = getNoOfBadAnswers(dct, word)
            if g == 0 and b == 0:
                priority = 0
            else:
                priority = calculatePriority(g, b)
            hq.heappush(queue, (priority, word))

    priority = 0
    tempQueue = []
    sortedQueue = []
    while len(queue):
        item = hq.heappop(queue)
        if priority == item[0]:
            tempQueue.append(item)
        else:
            priority = item[0]
            random.shuffle(tempQueue)
            sortedQueue += tempQueue
            tempQueue = [item]

    random.shuffle(tempQueue)
    sortedQueue += tempQueue
    return sortedQueue


def goodAnswer(dct, word):
    # print('Good!')
    g = getNoOfGoodAnswers(dct, word) + 1
    setNoOfGoodAnswers(dct, word, g)


def badAnswer(dct, word):
    print('\nBad! The commutator is:\t%s' % getAlg(dct, word))
    input('\nPress any key to continue...')
    b = getNoOfBadAnswers(dct, word) + 1
    setNoOfBadAnswers(dct, word, b)


def resetPoints(dct):
    os.system('cls')
    for word in dct[CORNERS]:
        setNoOfGoodAnswers(dct, word, 0)
        setNoOfBadAnswers(dct, word, 0)
    print('Scores set to 0')
    saveDict(dct)


def createDctBackUp(dct):
    os.system('cls')
    f = open(PATH_TO_BACKUP_JSON, 'w', encoding='utf-8')
    json.dump(dct, f, indent=8, ensure_ascii=False)
    f.close()
    print('Backup done!')
    input('Press enter to continue...')


def mainMenu(dct):

    while True:
        os.system('cls')
        print(MAIN_MENU)
        cmd = input('> ')
        if cmd == '1':
            train(dct)
        elif cmd == '2':
            addAlgs(dct)
        elif cmd == '3':
            checkAlgs(dct)
        elif cmd == '4':
            sortDict(dct)
        elif cmd == '5':
            resetPoints(dct)
        elif cmd == '6':
            createDctBackUp(dct)
        elif cmd == '0':
            saveAndExit(dct)


if __name__ == '__main__':
    os.system('cls')
    dctJSON = loadJSON()
    if not dctJSON:
        exit(1)

    mainMenu(dctJSON)
