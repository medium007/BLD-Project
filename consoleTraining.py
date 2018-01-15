import json

f = open('data/corners.json', 'r', encoding='utf-8')
dct = json.load(f)
f.close()

type = ['8', '1s', '>1s', '10+', '12+', 'alg']

workingType = 0
allType = True


def train():
    workWithType()

    for word in dct['corners']:
        if getScore(word) == 0:
            if allType or getType(word) == type[workingType]:
                a = input('%s: ' % word)
                if a == '':
                    setScore(word, 1)
                    saveDict()
                elif a == 'x':
                    saveAndExit()


def addAlgs():
    for word in dct['corners']:
        if not getAlg(word):    # and getSticker1(word) in ['T', 'W', 'Z']:
            print('Word %s' % word)
            setup = input('Setup: ')
            if setup == 'exit':
                saveAndExit()
            alg1 = input('Alg1: ')
            alg2 = input('Alg2: ')

            setAlg(word, createCom(setup, alg1, alg2))
            addMirrorAlg(setup, alg1, alg2, getSticker2(word), getSticker1(word))
    print('All words have an alg')


def getAlg(word):
    return dct.get('corners').get(word).get('alg')


def setAlg(word, alg):
    dct.get('corners').get(word).update({'alg': alg})


def getScore(word):
    return dct.get('corners').get(word).get('score')


def setScore(word, n):
    dct.get('corners').get(word).update({'score': n})


def saveAndExit():
    saveDict()
    exit()


def saveDict():
    f = open('D:/sandbox/BLD Project/jsonfile.txt', 'w', encoding='utf-8')
    json.dump(dct, f, indent=8, ensure_ascii=False)
    f.close()
    print('Dictionary saved!')
    input("Press Enter to continue...")


def workWithType():
    global workingType
    global allType
    workingType = int(input('Train type:'))
    if workingType == 6:
        allType = True
    else:
        allType = False


def getType(word):
    return dct.get('corners').get(word).get('type')


def createCom(setup, alg1, alg2):
    com = ''
    if(setup):
        com = '%s %s:' % (com, setup)
    if(alg2):
        com = '%s [ %s, %s ]' % (com, alg1, alg2)
    else:
        com = '%s ( %s )' % (com, alg1)
    return com


def getSticker1(word):
    return dct.get('corners').get(word).get('sticker1')


def getSticker2(word):
    return dct.get('corners').get(word).get('sticker2')


def setSticker1(word, sticker):
    dct.get('corners').get(word).update({'sticker1': sticker})


def setSticker2(word, sticker):
    dct.get('corners').get(word).update({'sticker2': sticker})


def addCorn():
    for word in dct['corners']:
        if getSticker1(word) == None:
            sticker = input('%s: ' % word)
            if sticker == 'x':
                saveAndExit()
            setSticker1(word, sticker[0].upper())
            setSticker2(word, sticker[1].upper())
    print('All corners have a stickers')


def testQ():
    count = 0
    for word in dct['corners']:
        if dct.get('corners').get(word).get('sticker1') in ['A', 'B', 'C']:
            count +=1
            print('%s\t%s' % (word, getAlg(word)))
    print(count)


def addMirrorAlg(setup, alg1, alg2, sticker1, sticker2):
    for word in dct['corners']:
        if getSticker1(word) == sticker1 and getSticker2(word) == sticker2:
            if alg2:
                comm = createCom(setup, alg2, alg1)
                setAlg(word, comm)
                print('Created mirror comm for %s : %s' % (word, comm))
                return
            else:
                print('Not created mirror comm for %s' % word)
                return


def isChecked(word):
    return dct.get('corners').get(word).get('checked')


def checkAlgs():
    for word in dct['corners']:
        if not isChecked(word):
            print('%s: %s' % (word, getAlg(word)))
            cmd = input('Is it correct?')
            if cmd == 'n' or cmd == 'N':
                removeAlg(word)
                addAlgs()
            elif cmd == 'e' or cmd == 'E':
                saveAndExit()
            else:
                setChecked(word)


def setChecked(word, toSet='yes'):
    dct.get('corners').get(word).update({'checked': toSet})


def removeAlg(word):
    setAlg(word, '')


def sortDict():
    global dct
    newDct = {'corners': {}}
    for i in range(ord('A'), ord('Z') + 1):
        for j in range(ord('A'), ord('Z') + 1):
            for word in dct['corners']:
                if getSticker1(word) == chr(i) and getSticker2(word) == chr(j):
                    newDct.get('corners').update({word: dct.get('corners')[word]})
                    # print(dct.get('corners')[word])
                    break
    print(newDct)
    dct = newDct
    saveAndExit()

if __name__ == '__main__':
    comm = input('Give a commend(t/a/c/q): ')
    if comm == 't':
        train()
    elif comm == 'a':
        addAlgs()
    elif comm == 'c':
        addCorn()
    elif comm == 'q':
        testQ()
    elif comm == 'u':
        checkAlgs()
    elif comm == 's':
        sortDict()
    else:
        exit()
    saveAndExit()
