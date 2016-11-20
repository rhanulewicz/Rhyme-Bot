import codecs
import sys
import time
import _pickle as pickle
import os
import json

def insertString(phrase, root):
    currentNode = root
    for sound in phrase:
        if sound not in currentNode[1]:
            currentNode[1][sound] = [False, {}, False]
        currentNode = currentNode[1][sound]
    currentNode[0] = True

def nonRecursiveFind(phrase, root):
    currentNode = root
    currentSuffix = []
    i = 0
    offTrack = False
    while True:
        allChildrenCovered = True
        for child in currentNode[1]:
            if not currentNode[1][child][2]:
                allChildrenCovered = False
                break
        if currentNode == root[1][phrase[0]] and allChildrenCovered == True:
            loadAdjacent(phrase, root)
            return []
        #if root is a phrase and (there are no children OR all children are covered),
        #return the phrase and mark it as covered
        if currentNode[0] and (len(currentNode[1]) == 0 or allChildrenCovered):
            currentNode[2] = True
            return currentSuffix
        if offTrack == False:
            if phrase[i] not in currentNode[1]:
                offTrack = True
        if offTrack == True:                                                #if sound not in children
            if allChildrenCovered == False:                                 #and there are other unmarked children
                for child in currentNode[1]:
                    if currentNode[1][child][2] == False:
                        currentNode = currentNode[1][child]                 #proceed to the first unmarked child
                        currentSuffix += [child]
                        break
            else:                                                           #if there are no other unmarked children,
                currentNode[2] = True                                       #mark current node. There's nowhere to go.
                return currentSuffix
        else:                                                               #if sound is in children,
            if not currentNode[1][phrase[i]][2]:                                #and it's not marked
                currentNode = currentNode[1][phrase[i]]                      #proceed to that node
                currentSuffix += [phrase[i]]
                if i+1 < len(phrase):
                    i = i + 1
            else:
                offTrack = True
    return currentSuffix

#Returns a dictionary with words as keys and lists of sounds as values
def parseDictionary():
    words = codecs.open(sys.argv[1], 'r', encoding='iso-8859-1')
    dict = {}
    for line in words.readlines():
        split_line = line.split(" ")
        if (split_line[0][0].isalpha() or split_line[0][0].isdigit()) and ("(" not in split_line[0]):
            itersounds = iter(split_line)
            next(itersounds)
            next(itersounds)
            ls = []
            for sound in itersounds:
                sound = sound[0:2].strip()
                ls.append(sound.strip())
            dict[split_line[0].lower()] = ls
    return dict

#Returns list of sounds from the input phrase in reverse for easy suffix trie traversal
def convertInputPhrase(dictionary):
    dict = dictionary
    words = sys.argv[4].split("_")
    soundlist = []
    for word in words:
        word = word.lower()
        soundlist = soundlist + dict[word]
    soundlist.reverse()
    return soundlist

#Returns a dictionary with backwards tuples of sounds as keys and phrases as values.
#This makes it easier to look up the results of the suffix tree search
def parsePhrases(dictionary):
    dict = dictionary
    phrases = codecs.open(sys.argv[2], 'r', encoding='iso-8859-1')
    dictOut = {}
    for line in phrases.readlines():
        phrase = str(line.strip())
        words = line.split(" ")
        ls = []
        for word in words:
            ls = ls + dict[word.strip()]
        ls.reverse()
        dictOut[tuple(ls)] = phrase
    return dictOut

def buildSuffixTrie(phraseDictionary, root):
    rootNode = root
    phraseDict = phraseDictionary
    for phrase in phraseDict:
        insertString(phrase,rootNode)

#def topK():
def loadAdjacent(phrase, root):
    for i in os.listdir(os.getcwd()):
        if i.startswith(str(phrase[0]) + "_"):
            splitString = str(i).split("_")
            secondHalf = splitString[1]
            strippedHalf = secondHalf[:len(secondHalf)-7]
            pickle_in = open(i, "rb")
            root[1][phrase[0]][1][strippedHalf] = pickle.load(pickle_in)
            pickle_in.close()

timeStart = time.time()
root = [False, {}, False] #[isString, Children, isCovered]

if not os.path.isfile('data/generated/dict.pickle'):
    dict = parseDictionary()
    pickle_out = open("data/generated/dict.pickle","wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()
else:
    pickle_in = open("data/generated/dict.pickle", 'rb')
    dict = pickle.load(pickle_in)
    pickle_in.close()

inputPhrase = convertInputPhrase(dict)

if not os.path.isfile('data/generated/phraseDict.pickle'):
    phraseDict = parsePhrases(dict)
    pickle_out = open("data/generated/phraseDict.pickle","wb")
    pickle.dump(phraseDict, pickle_out)
    pickle_out.close()
else:
    pickle_in = open("data/generated/phraseDict.pickle",'rb')
    phraseDict = pickle.load(pickle_in)
    pickle_in.close()


if not os.path.isfile('data/generated/trieNodeList.pickle'):
    buildSuffixTrie(phraseDict,root)
    nodeList = []
    pickle_out = open('data/generated/trieNodeList.pickle', 'wb')
    pickle.dump(nodeList, pickle_out)
    pickle_out.close()
    for subtree in root[1]:
        for subsubtree in root[1][subtree][1]:
            pickle_out = open("data/generated/" + str(subtree) + "_" + str(subsubtree) + ".pickle", "wb")
            pickle.dump(root[1][subtree][1][subsubtree], pickle_out)
            pickle_out.close()
else:
    pickle_in = open("data/generated/" + str(inputPhrase[0]) + "_" + str(inputPhrase[1]) + ".pickle", "rb")
    root[1][inputPhrase[0]] = [False, {}, False]
    root[1][inputPhrase[0]][1][inputPhrase[1]] = pickle.load(pickle_in)
    pickle_in.close()
k = 0
while(k != int(sys.argv[3])):
    search = tuple(nonRecursiveFind(inputPhrase,root))
    if search in phraseDict:
        print(phraseDict[search])
        k = k + 1

print("Completed in " + str(time.time() - timeStart) + " seconds.")






