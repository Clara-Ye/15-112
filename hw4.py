#################################################
# hw4.py
#
# Your name: Clara Ye
# Your andrew id: zixuany
#################################################

import cs112_s20_unit4_linter
import basic_graphics
import string, copy, random, math

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

#################################################
# Person class
#################################################

class Person(object):

    # a person has properties name, age, friends, and friendsNames:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = []
        self.friendsNames = []
    
    # returns the name of a given person:
    def getName(self):
        return self.name
    
    # returns the age of a given person:
    def getAge(self):
        return self.age
    
    # returns a list of friends of a given person:
    def getFriends(self):
        return self.friends
    
    # returns a list of the names of friends of a given person:
    def getFriendsNames(self):
        return self.friendsNames
    
    # adds a friend to a person:
    def addFriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            self.friendsNames.append(friend.name)
            self.friendsNames.sort()
            # adds the person to the friend's freinds:
            friend.friends.append(self)
            friend.friendsNames.append(self.name)
            friend.friendsNames.sort()
    
    # adds all the friends of a given person to a person:
    def addFriends(self, person):
        for friend in person.friends:
            self.addFriend(friend)
    
#################################################
# removeEvens
#################################################

# removes the even numbers in a list destructively:
def destructiveRemoveEvens(L):
    i = 0
    while (i < len(L)):
        if (L[i] % 2 == 0):
            L.pop(i)
        else:
            i += 1

# removes the even numbers in a list nondestructively:
def nondestructiveRemoveEvens(L):
    N = []
    for num in L:
        if (num % 2 != 0):
            N.append(num) 
    return N

#################################################
# bestScrabbleScore
#################################################

# checks if a word can be constructed using a hand:
def isConstructable(word, hand):
    for char in word:
        if (char not in hand):
            return False
        elif (word.count(char) > hand.count(char)):
            return False
    return True

def testIsConstructable():
    print("Testing isConstuctable()...", end = "")
    assert(isConstructable("a", ["a"]) == True)
    assert(isConstructable("a", ["b"]) == False)
    assert(isConstructable("cat", ["c", "a", "t"]) == True)
    assert(isConstructable("cat", ["a", "b", "c", "d", "t"]) == True)
    assert(isConstructable("catt", ["a", "b", "c", "d", "t"]) == False)
    print("Passed!")

# calculates the total letter score of a word:
def calculateScore(word, letterScores):
    score = 0
    for c in word:
        index = ord(c) - ord("a")
        score += letterScores[index]
    return score

def testCalculateScore():
    print("Testing calculateScore()...", end = "")
    assert(calculateScore("a", ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])) == 1)
    assert(calculateScore("xyz", ([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 
                                   1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1])) == 10)
    assert(calculateScore("zzy", ([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5,
                                   1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1])) == 7)
    print("Passed!")

# returns the highest scoring word(s) that can be constucted
# given a dictionary of legal words, a list of letter scores, and a hand:
def bestScrabbleScore(dictionary, letterScores, hand):
    bestScore = -1
    for word in dictionary:
        if isConstructable(word, hand):
            currScore = calculateScore(word, letterScores)
            # update best variables when needed:
            if (currScore > bestScore):
                bestScore = currScore
                bestScrabble = (word, currScore)
            elif (currScore == bestScore):
                if isinstance(bestScrabble[0], str):
                    # create a list of words:
                    bestScrabble = ([bestScrabble[0], word], currScore)
                else:
                    # add word to existing list:
                    bestScrabble = (bestScrabble[0]+[word], currScore)
    if (bestScore == -1):
        return None
    return bestScrabble

#################################################
# solvesCryptarithm
#################################################

# takes a cryptarithm and returns a list of the 3 words in it:
def extractWords(puzzle):
    i1 = puzzle.find(" ")
    # 2 spaces and 1 operater gives the 3 index distance
    i2 = puzzle.find(" ", i1+3)
    return [puzzle[:i1], puzzle[i1+3:i2], puzzle[i2+3:]]

def testExtractWords():
    print("Testing extractWords()...", end = "")
    assert(extractWords("RAM + RAT = ANT") == ["RAM", "RAT", "ANT"])
    assert(extractWords("ANT + CAT = EEL") == ["ANT", "CAT", "EEL"])
    assert(extractWords("SEND + MORE = MONEY") == ["SEND", "MORE", "MONEY"])
    print("Passed!")

# replaces words in cryptarithm with the corresponding digit in the solution:
def assignDigits(wordList, solution):
    numList = []
    for word in wordList:
        num = ""
        for c in word:
            i = solution.find(c)
            num += str(i)
        numList.append(int(num))
    return numList

def testAssignDigits():
    print("Testing assignDigits()...", end = "")
    assert(assignDigits(["RAM", "RAT", "ANT"], "MRATN-----") == [120, 123, 243])
    assert(assignDigits(["ANT", "CAT", "EEL"], "LANCET----") == [125, 315, 440])
    assert(assignDigits(["SEND", "MORE", "MONEY"], "OMY--ENDRS") == 
                        [9567, 1085, 10652])
    print("Passed!")

# checks if a solution solves a cryptarithm:
def solvesCryptarithm(puzzle, solution):
    wordList = extractWords(puzzle)
    # avoids crashing with unmatched letters:
    for word in wordList:
        for c in word:
            if c not in solution:
                return False
    numList = assignDigits(wordList, solution)
    return (numList[0] + numList[1] == numList[2])

#################################################
# drawLetterTypePieChart(canvas)
#################################################

def drawLetterTypePieChart(canvas, text, cx, cy, r):
    return 42

#################################################
# spicy combinatorics problems
#################################################

# takes a number in decimal and returns its kth digit in binary:
def getKthBinaryDigit(n, k):
    return ((n // (2**k)) % 2)

# takes a list and generates all of its sublists:
def allSublists(L):
    for n in range(2**len(L)):
        sublist = []
        for k in range(len(L)):
            # include the kth element in L if the kth binary digit of n is 1:
            if (getKthBinaryDigit(n, k) == 1):
                sublist.append(L[k])
        yield sublist

# returns a sublist of L that sums to 0:
def solveSubsetSum(L):
    for sublist in allSublists(L):
        if (sublist != []) and (sum(sublist) == 0):
            return sublist
    return None

# generates all permutations of a list of elements:
def heapsAlgorithmForPermutations(L):
    # algorithm from https://en.wikipedia.org/wiki/Heap%27s_algorithm
    # codes from https://piazza.com/class/k4cogezbi4h3jk?cid=665
    n = len(L)
    c = [0]*n
    A = copy.copy(L)
    yield copy.copy(A)
    i = 0
    while i < n:
        if  c[i] < i:
            if (i%2 == 0):
                A[0], A[i] = A[i], A[0]
            else:
                A[c[i]], A[i] = A[i], A[c[i]]
            yield copy.copy(A)
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1

# takes a list of words and returns a string of the unique letters:
def getUniqueLetters(L):
    uniLetters = ""
    for word in L:
        for c in word:
            if c not in uniLetters:
                uniLetters += c
    return uniLetters

def testgetUniqueLetters():
    print("  Testing getUniqueLetters()...", end = "")
    assert(getUniqueLetters(["RAM", "RAT", "ANT"]) == "RAMTN")
    assert(getUniqueLetters(["ANT", "CAT", "EEL"]) == "ANTCEL")
    assert(getUniqueLetters(["SEND", "MORE", "MONEY"]) == "SENDMORY")
    print("Passed!")

# augments a string with dashes so it is of given length:
def augmentString(s, length):
    return (s + "-" * (length - len(s)))

def testAugmentString():
    print("  Testing augmentString()...", end = "")
    assert(augmentString("RAMTN", 10) == "RAMTN-----")
    assert(augmentString("ANTCEL", 7) == "ANTCEL-")
    assert(augmentString("SENDMORY", 8) == "SENDMORY")
    print("Passed!")

# returns a more-nicely-formatted version of the solution:
def formatSolution(puzzle, solution):
    wordList = extractWords(puzzle)
    numList = assignDigits(wordList, solution)
    return f"{puzzle}\n{numList[0]} + {numList[1]} = {numList[2]}"

def testFormatSolution():
    print("  Testing formatSolution()...", end = "")
    assert(formatSolution("RAM + RAT = ANT", "MRATN-----") == """\
RAM + RAT = ANT
120 + 123 = 243""")
    assert(formatSolution("ANT + CAT = EEL", "LANCET----") == """\
ANT + CAT = EEL
125 + 315 = 440""")
    print("Passed!")    

# turns a list of single characters into a string:
def listToStr(L):
    result = ""
    for s in L:
        result += s
    return result

# solves a cryptarithm with only digits smaller than maxDigit:
def solveCryptarithmWithMaxDigit(puzzle, maxDigit):
    wordList = extractWords(puzzle)
    uniLetters = getUniqueLetters(wordList)
    if (len(uniLetters) > maxDigit+1):
        return None
    else:
        augString = augmentString(uniLetters, maxDigit+1)
        for solutionList in heapsAlgorithmForPermutations(list(augString)):
            solutionStr = listToStr(solutionList)
            solutionStr = augmentString(solutionStr, 10)
            if solvesCryptarithm(puzzle, solutionStr):
                return formatSolution(puzzle, solutionStr)
        return None

# finds all solutions to a cryptarithm with maxDigit,
# returns all the solutions and the number of solutions:
def countCryptarithmsWithMaxDigit(puzzle, maxDigit):
    wordList = extractWords(puzzle)
    uniLetters = getUniqueLetters(wordList)
    if (len(uniLetters) > maxDigit+1):
        return None
    else:
        augString = augmentString(uniLetters, maxDigit+1)
        count = 0
        solutions = ""
        for solutionList in heapsAlgorithmForPermutations(list(augString)):
            solutionStr = listToStr(solutionList)
            solutionStr = augmentString(solutionStr, 10)
            if solvesCryptarithm(puzzle, solutionStr):
                solutions += formatSolution(puzzle, solutionStr)
                count += 1
        return (solutions, count)

# gets all legal cryptarithms with a single solution given a list of words:
def getAllSingletonCryptarithmsWithMaxDigit(words, maxDigit):
    words = sorted(words)
    result = ""
    for iN1 in range(len(words)-1):
        for iN2 in range(iN1+1, len(words)):
            for iResult in range(len(words)):
                if ((words[iResult] != words[iN1]) and
                    (words[iResult] != words[iN2])):
                    puzzle = f"{words[iN1]} + {words[iN2]} = {words[iResult]}"
                    solution = countCryptarithmsWithMaxDigit(puzzle, maxDigit)
                    if (solution != None) and (solution[1] == 1):
                        result += f"{solution[0]}\n"
    result = result.strip()
    return result

#################################################
# spicy runSimpleProgram
#################################################

def runSimpleProgram(program, args):
    return 42

#################################################
# Test Functions
#################################################

def testPersonClass():
    print('Testing Person Class...', end='')
    fred = Person('fred', 32)
    assert(isinstance(fred, Person))
    assert(fred.getName() == 'fred')
    assert(fred.getAge() == 32)
    # Note: person.getFriends() returns a list of Person objects who
    #       are the friends of this person, listed in the order that
    #       they were added.
    # Note: person.getFriendNames() returns a list of strings, the
    #       names of the friends of this person.  This list is sorted!
    assert(fred.getFriends() == [ ])
    assert(fred.getFriendsNames() == [ ])

    wilma = Person('wilma', 35)
    assert(wilma.getName() == 'wilma')
    assert(wilma.getAge() == 35)
    assert(wilma.getFriends() == [ ])

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred])
    assert(wilma.getFriendsNames() == ['fred'])
    assert(fred.getFriends() == [wilma]) # friends are mutual!
    assert(fred.getFriendsNames() == ['wilma'])

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred]) # don't add twice!

    betty = Person('betty', 29)
    fred.addFriend(betty)
    assert(fred.getFriendsNames() == ['betty', 'wilma'])

    pebbles = Person('pebbles', 4)
    betty.addFriend(pebbles)
    assert(betty.getFriendsNames() == ['fred', 'pebbles'])

    barney = Person('barney', 28)
    barney.addFriend(pebbles)
    barney.addFriend(betty)
    barney.addFriends(fred) # add ALL of Fred's friends as Barney's friends
    assert(barney.getFriends() == [pebbles, betty, wilma])
    assert(barney.getFriendsNames() == ['betty', 'pebbles', 'wilma'])
    fred.addFriend(wilma)
    fred.addFriend(barney)
    assert(fred.getFriends() == [wilma, betty, barney])
    assert(fred.getFriendsNames() == ['barney', 'betty', 'wilma']) # sorted!
    assert(barney.getFriends() == [pebbles, betty, wilma, fred])
    assert(barney.getFriendsNames() == ['betty', 'fred', 'pebbles', 'wilma'])
    print('Passed!')

def _destructiveRemoveEvens(L):
    destructiveRemoveEvens(L)
    return L

def testDestructiveRemoveEvens():
    print("Testing destructiveRemoveEvens()...", end="")
    assert(_destructiveRemoveEvens([1,2,3,4]) == [1,3])
    assert(_destructiveRemoveEvens([1,3,5,7,3]) == [1,3,5,7,3])
    assert(_destructiveRemoveEvens([2,4,2,4,6]) == [ ])
    assert(_destructiveRemoveEvens([2,4,1,2,4,6]) == [1])
    print("Passed!")

def _verifyRemoveEvensIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    nondestructiveRemoveEvens(a) # ignore result, just check if destructive
    return (a == b)

def testNondestructiveRemoveEvens():
    print("Testing nondestructiveRemoveEvens()...", end='')
    assert(_verifyRemoveEvensIsNondestructive())
    assert(nondestructiveRemoveEvens([1,2,3,4]) == [1,3])
    assert(nondestructiveRemoveEvens([1,3,5,7,3]) == [1,3,5,7,3])
    assert(nondestructiveRemoveEvens([2,4,2,4,6]) == [ ])
    assert(nondestructiveRemoveEvens([2,4,1,2,4,6]) == [1])
    print("Passed!")

def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"] 
    def letterScores2(): return [1+(i%5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) ==
                                        (["a", "c"], 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) ==
                                        None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) ==
                                         (["xyz", "zxy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) ==
                                        (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) ==
                                        ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) ==
                                        ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) ==
                                        None)
    print("Passed!")

def testSolvesCryptarithm():
    print("Testing solvesCryptarithm()...", end="")
    assert(solvesCryptarithm("SEND + MORE = MONEY","OMY--ENDRS") == 
                                  True)
    # from http://www.cryptarithms.com/default.asp?pg=1
    assert(solvesCryptarithm("NUMBER + NUMBER = PUZZLE", "UMNZP-BLER") ==
                                  True)
    assert(solvesCryptarithm("TILES + PUZZLES = PICTURE", "UISPELCZRT") ==
                                  True)
    assert(solvesCryptarithm("COCA + COLA = OASIS", "LOS---A-CI") ==
                                  True)
    assert(solvesCryptarithm("CROSS + ROADS = DANGER", "-DOSEARGNC") ==
                                  True)

    assert(solvesCryptarithm("SEND + MORE = MONEY","OMY--ENDR-") == False)
    assert(solvesCryptarithm("SEND + MORE = MONEY","OMY-ENDRS") == False)
    assert(solvesCryptarithm("SEND + MORE = MONY","OMY--ENDRS") == False)
    assert(solvesCryptarithm("SEND + MORE = MONEY","MOY--ENDRS") == False)
    assert(solvesCryptarithm("CROSS + ROADS = DANGER", "-DOSEA-GNC") == False)
    print("Passed!")

def drawLetterTypePieCharts(canvas, width, height):
    r = min(width,height)*0.2
    canvas.create_line(width/2, 0, width/2, height)
    canvas.create_line(0, height/2, width, height/2)
    drawLetterTypePieChart(canvas, "AB, c de!?!", width/4, height/4, r)
    drawLetterTypePieChart(canvas, "AB e", width/4, height*3/4, r)
    drawLetterTypePieChart(canvas, "A", width*3/4, height/4, r)
    drawLetterTypePieChart(canvas, "               ", width*3/4, height*3/4, r)

def testDrawLetterTypePieChart():
    print('Testing drawLetterTypePieChart()...')
    basic_graphics.run(drawFn=drawLetterTypePieCharts, width=800, height=800)
    print('Do a visual inspection to verify this passed!')

def testAllSublists():
    print('  Testing allSublists()...', end='')
    def f(): yield 42
    assert(type(allSublists([1,2,3])) == type(f())) # generator
    assert(sorted(allSublists([1])) == [ [], [1] ])
    assert(sorted(allSublists([3, 5])) == [ [], [3], [3, 5], [5] ])
    assert(sorted(allSublists([6,7,8])) == [ [], [6], [6, 7], [6, 7, 8],
                                             [6, 8], [7], [7, 8], [8] ])
    print('Passed!')

def testSolveSubsetSum():
    def checkSubsetSum(L):
        solution = solveSubsetSum(L)
        for v in solution:
            assert(solution.count(v) <= L.count(v))
        assert(sum(solution) == 0)
    print('  Testing solveSubsetSum()...', end='')
    assert(solveSubsetSum([5,2,3,-4]) == None)
    checkSubsetSum([-1,5,2,3,-4])
    checkSubsetSum([8,19,31,27,52,-70,4])
    print('Passed!')

def testHeapsAlgorithmForPermutations():
    print('  Testing heapsAlgorithmForPermutations()...', end='')
    def f(): yield 42
    assert(type(heapsAlgorithmForPermutations([1])) == type(f())) # generator
    assert(sorted(heapsAlgorithmForPermutations([1])) == [[1]])
    assert(sorted(heapsAlgorithmForPermutations([1,2])) == [
            [1,2], [2,1]
        ])
    assert(sorted(heapsAlgorithmForPermutations([3,1,2])) == [
            [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]
        ])
    print('Passed!')

def testSolveCryptarithmWithMaxDigit():
    print('  Testing solveCryptarithmWithMaxDigit()...', end='')
    assert(solveCryptarithmWithMaxDigit('RAM + RAT = ANT', 4) == '''\
RAM + RAT = ANT
120 + 123 = 243''')
    assert(solveCryptarithmWithMaxDigit('ANT + CAT = EEL', 4) == None)
    assert(solveCryptarithmWithMaxDigit('ANT + CAT = EEL', 5) == '''\
ANT + CAT = EEL
125 + 315 = 440''')
    print('Passed!')

def testGetAllSingletonCryptarithmsWithMaxDigit():
    print('  Testing getAllSingletonCryptarithmsWithMaxDigit()...', end='')
    words = ['EEL', 'RAM', 'CAT', 'BEE', 'FLY',
             'HEN', 'RAT', 'DOG', 'ANT']
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 3) == '')
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 4) == '''\
RAM + RAT = ANT
120 + 123 = 243''')
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 5) == '''\
ANT + CAT = EEL
125 + 315 = 440
ANT + CAT = HEN
105 + 315 = 420
ANT + RAT = EEL
125 + 315 = 440
ANT + RAT = HEN
105 + 315 = 420
BEE + EEL = FLY
411 + 112 = 523''')

    words = ['DEER', 'BEAR', 'GOAT', 'MULE', 'PUMA',
             'COLT', 'ORCA', 'IBEX', 'LION', 'WOLF']
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 5) == '')
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 6) == '''\
BEAR + DEER = IBEX
4203 + 1223 = 5426
COLT + GOAT = ORCA
4635 + 1605 = 6240''')
    print('Passed!')

def testSpicyCombinatoricsProblems():
    print('Testing spicy combinatorics problems...')
    testAllSublists()
    testSolveSubsetSum()
    testHeapsAlgorithmForPermutations()
    testgetUniqueLetters()
    testAugmentString()
    testFormatSolution()
    testSolveCryptarithmWithMaxDigit()
    testGetAllSingletonCryptarithmsWithMaxDigit()
    print('Passed!')

def testRunSimpleProgram():
    print("Testing runSimpleProgram()...", end="")
    largest = """! largest: Returns max(A0, A1)
                   L0 - A0 A1
                   JMP+ L0 a0
                   RTN A1
                   a0:
                   RTN A0"""
    assert(runSimpleProgram(largest, [5, 6]) == 6)
    assert(runSimpleProgram(largest, [6, 5]) == 6)

    sumToN = """! SumToN: Returns 1 + ... + A0
                ! L0 is a counter, L1 is the result
                L0 0
                L1 0
                loop:
                L2 - L0 A0
                JMP0 L2 done
                L0 + L0 1
                L1 + L1 L0
                JMP loop
                done:
                RTN L1"""
    assert(runSimpleProgram(sumToN, [5]) == 1+2+3+4+5)
    assert(runSimpleProgram(sumToN, [10]) == 10*11//2)
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    # required
    testPersonClass()

    # mild
    testDestructiveRemoveEvens()
    testNondestructiveRemoveEvens()

    # medium
    testIsConstructable()
    testCalculateScore()
    testBestScrabbleScore()
    testExtractWords()
    testAssignDigits()
    testSolvesCryptarithm()
    #testDrawLetterTypePieChart()

    # spicy
    testSpicyCombinatoricsProblems()
    #testRunSimpleProgram()

def main():
    cs112_s20_unit4_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
