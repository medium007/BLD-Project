import json

TYPES = ['8', '1s', '>1s', '10+', '12+', 'alg', 'All types']
ALL_TYPES = TYPES[-1]
PATH_TO_JSON = 'data/corners.json'


def loadJSON():
    f = open(PATH_TO_JSON, 'r', encoding='utf-8')
    dct = json.load(f)
    f.close()
    return dct


def train(dct):
    workingType = workWithType()
    for word in dct['corners']:
        if getScore(dct, word) == 0:
            if TYPES[workingType] == ALL_TYPES or TYPES[workingType] == getType(dct, word):
                a = input('%s: ' % word)
                if a == '':
                    setScore(dct, word, 1)
                    saveDict(dct)
                elif a == 'x':
                    saveAndExit(dct)


def addAlgs(dct):
    for word in dct['corners']:
        if not getAlg(dct, word):    # and getSticker1(word) in ['T', 'W', 'Z']:
            print('Word %s' % word)
            setup = input('Setup: ')
            if setup == 'exit':
                saveAndExit(dct)
            alg1 = input('Alg1: ')
            alg2 = input('Alg2: ')

            setAlg(dct, word, createCom(setup, alg1, alg2))
            addMirrorAlg(dct, setup, alg1, alg2, getSticker2(dct, word), getSticker1(dct, word))
    print('All words have an alg')


def getAlg(dct, word):
    return dct.get('corners').get(word).get('alg')


def setAlg(dct, word, alg):
    dct.get('corners').get(word).update({'alg': alg})


def getScore(dct, word):
    return dct.get('corners').get(word).get('score')


def setScore(dct, word, n):
    dct.get('corners').get(word).update({'score': n})


def saveAndExit(dct):
    saveDict(dct)
    exit()


def saveDict(dct):
    f = open(PATH_TO_JSON, 'w', encoding='utf-8')
    json.dump(dct, f, indent=8, ensure_ascii=False)
    f.close()
    print('Dictionary saved!')
    input("Press Enter to continue...")


def workWithType():
    print('List of available types of commutators:\n'
          '\t1 - 8 moves\n'
          '\t2 - 8 moves with 1 setup\n'
          '\t3 - 8 moves with more than 1 setup\n'
          '\t4 - 10 moves (including with setups)\n'
          '\t5 - 12 moves (including with setups)\n'
          '\t6 - Variations of permutation A\n'
          '\t7 - All of above types')
    workingType = int(input('Train type: ')) - 1
    return workingType


def getType(dct, word):
    return dct.get('corners').get(word).get('type')


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
    return dct.get('corners').get(word).get('sticker1')


def getSticker2(dct, word):
    return dct.get('corners').get(word).get('sticker2')


def setSticker1(dct, word, sticker):
    dct.get('corners').get(word).update({'sticker1': sticker})


def setSticker2(dct, word, sticker):
    dct.get('corners').get(word).update({'sticker2': sticker})


def addCorn(dct):
    for word in dct['corners']:
        if getSticker1(dct, word) == None:
            sticker = input('%s: ' % word)
            if sticker == 'x':
                saveAndExit(dct)
            setSticker1(dct, word, sticker[0].upper())
            setSticker2(dct, word, sticker[1].upper())
    print('All corners have a stickers')


def testQ(dct):
    count = 0
    for word in dct['corners']:
        if dct.get('corners').get(word).get('sticker1') in ['A', 'B', 'C']:
            count +=1
            print('%s\t%s' % (word, getAlg(dct, word)))
    print(count)


def addMirrorAlg(dct, setup, alg1, alg2, sticker1, sticker2):
    for word in dct['corners']:
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
    return dct.get('corners').get(word).get('checked')


def checkAlgs(dct):
    for word in dct['corners']:
        if not isChecked(dct, word):
            print('%s: %s' % (word, getAlg(dct, word)))
            cmd = input('Is it correct?')
            if cmd == 'n' or cmd == 'N':
                removeAlg(dct, word)
                addAlgs(dct)
            elif cmd == 'e' or cmd == 'E':
                saveAndExit(dct)
            else:
                setChecked(dct, word)


def setChecked(dct, word, toSet='yes'):
    dct.get('corners').get(word).update({'checked': toSet})


def removeAlg(dct,word):
    setAlg(dct, word, '')


def sortDict(dct):
    newDct = {'corners': {}}
    for i in range(ord('A'), ord('Z') + 1):
        for j in range(ord('A'), ord('Z') + 1):
            for word in dct['corners']:
                if getSticker1(dct, word) == chr(i) and getSticker2(dct, word) == chr(j):
                    newDct.get('corners').update({word: dct.get('corners')[word]})
                    # print(dct.get('corners')[word])
                    break
    print(newDct)
    dct = newDct
    saveAndExit(dct)

if __name__ == '__main__':

    dctJSON = loadJSON()

    print('List of available commends:\n'
          '\t1 - Train commutators\n'
          '\t2 - Add commutators\n'
          '\t3 - Add corners?\n'
          '\t4 - Test?\n'
          '\t5 - Check correctness of commutators\n'
          '\t6 - Sort dictionary by stickers\n'
          '\t0 - exit\n')

    while True:
        cmd = input('> ')
        if cmd == '1':
            train(dctJSON)
        elif cmd == '2':
            addAlgs(dctJSON)
        elif cmd == '3':
            addCorn(dctJSON)
        elif cmd == '4':
            testQ(dctJSON)
        elif cmd == '5':
            checkAlgs(dctJSON)
        elif cmd == '6':
            sortDict(dctJSON)
        elif cmd == '0':
            saveAndExit(dctJSON)
