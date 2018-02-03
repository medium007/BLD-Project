import json
from constants import *
import os
from dictionary import Dictionary


def train(dct):
    workingType = workWithType()
    dct.createPriorityQueue(workingType)
    continueTraining = True

    while continueTraining:
        os.system('cls')
        word = dct.getWordFromQueue()
        print('Word:\t%s' % word)
        yn = input('Do you know it? (y/n): ')

        if yn == 'y' or yn == '':
            goodAnswer(dct, word)
        elif yn == 'n':
            badAnswer(dct, word)
        else:
            continueTraining = False

        dct.saveDict()

        if dct.getQueueLength() == 0:
            print('\nNo more left commutators.')
            yn = input('Do you want to continue? (y/n): ')
            if yn == 'y':
                dct.createPriorityQueue(workingType)
            else:
                continueTraining = False

    dct.saveDict()


def addAlgs(dct):
    os.system('cls')
    for word in dct.getWordsList():
        if not dct.getAlg(word):
            print('Word %s' % word)
            setup = input('Setup: ')
            if setup == 'exit':
                dct.saveDict()
                return
            alg1 = input('Alg1: ')
            alg2 = input('Alg2: ')

            dct.setAlg(word, dct.createCom(setup, alg1, alg2))
            if dct.addMirrorAlg(setup, alg1, alg2, dct.getSticker2(word), dct.getSticker1(word)):
                print('Added')
    print('All words have an alg')
    dct.saveDict()


def saveAndExit(dct):
    dct.saveDict()
    exit(0)


def workWithType():
    os.system('cls')
    print(WORKTYPE_MENU)
    workingType = int(input('> '))
    return workingType


def checkAlgs(dct):
    os.system('cls')
    for word in dct.getWordsList():
        if not dct.getChecked(word):
            print('\n%s: %s' % (word, dct.getAlg(word)))
            cmd = input('Is it correct?')
            if cmd == 'n' or cmd == 'N':
                dct.removeAlg(word)
                addAlgs(dct)
            elif cmd == 'e' or cmd == 'E':
                dct.saveDict()
                return
            else:
                dct.setChecked(word)

    print('All commutators are checked.')
    dct.saveDict()


def sortDict(dct):
    dct.sortWordsInDictionary()
    print('Dictionary sorted.')


def goodAnswer(dct, word):
    g = dct.getNoOfGoodAnswers(word) + 1
    dct.setNoOfGoodAnswers(word, g)


def badAnswer(dct, word):
    print('\nBad! The commutator is:\t%s' % dct.getAlg(word))
    input('\nPress any key to continue...')
    b = dct.getNoOfBadAnswers(word) + 1
    dct.setNoOfBadAnswers(word, b)


def resetPoints(dct):
    os.system('cls')
    for word in dct.getWordsList():
        dct.setNoOfGoodAnswers(word, 0)
        dct.setNoOfBadAnswers(word, 0)
    print('Scores set to 0')
    dct.saveDict()


def createDctBackUp(dct):
    os.system('cls')
    f = open(PATH_TO_BACKUP_JSON, 'w', encoding='utf-8')
    json.dump(dct.dict, f, indent=8, ensure_ascii=False)
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
    dctJSON = Dictionary()
    if not dctJSON:
        input('File (%s) not found, press any key to exit' %PATH_TO_JSON)
        exit(1)

    mainMenu(dctJSON)
