#################################################
# hw3.py
#
# Your name: Clara Ye
# Your andrew id: zixuany
#################################################

import cs112_s20_unit3_linter
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

# takes a row of data and returns the scorer's name and total score:
def getScore(line):
    score = 0
    scorer = None
    for item in line.split(","):
        if (item.isalpha()):
            scorer = item
        elif (item != ""):
            score += int(item)
    return (scorer, score)

# takes a string of csv data,
# returns the player(s) with the highest total score:
def topScorer(data):
    if (data == ""):
        # returns None if there is no data:
        return None
    else:
        topScore = -1
        topScorer = None
        for line in data.split("\n"):
            (scorer, score) = getScore(line)
            # update top score and top scorer when needed:
            if (score > topScore):
                topScore = score
                topScorer = scorer
            elif (score == topScore):
                topScorer += "," + scorer
        return topScorer

# wraps a text into a multi-line string with given width:
def wordWrap(text, width):
    if (len(text) <= width):
        return text
    else:
        wrappedText = ""
        for i in range(0, len(text), width):
            line = text[i:(i+width)]
            clearedLine = line.strip()
            dashedLine = clearedLine.replace(" ", "-")
            wrappedText += dashedLine + "\n"
        # remove the extra new line:
        wrappedText = wrappedText[:len(wrappedText)-1]
        return wrappedText

def longestSubpalindrome(s):
    return 42

# takes two strings and returns the number of exact and partial matches:
def getMatches(target, guess):
    exactMatch = 0
    partialMatch = 0
    matched = ""
    pending = ""
    for i in range(len(guess)):
        if (guess[i] == target[i]):
            exactMatch += 1
            matched += guess[i]
        elif (guess[i] in target):
            if (guess.count(guess[i]) <= target.count(guess[i])):
                partialMatch += 1
            elif (guess[i] not in pending):
                pending += guess[i]
    # add to partial match the no. of times 
    # each char in pending appears in target but unmatched:
    for char in pending:
        partialMatch += (target.count(char) - matched.count(char))
    return (exactMatch, partialMatch)

def testGetMatches():
    print("Testing getMatches()...",end = "")
    assert(getMatches('ccba', 'ddbc') == (1, 1))
    assert(getMatches('abcd', 'aabd') == (2, 1))
    assert(getMatches('wxyz', 'wxyz') == (4, 0))
    assert(getMatches("abcd", "bcda") == (0, 4))
    assert(getMatches('cdef', 'bccc') == (0, 1))
    print("Passed!")

# returns a string indicating the result of a single guess in Mastermind:
def mastermindScore(target, guess):
    (exactMatch, partialMatch) = getMatches(target, guess)
    if (exactMatch == 0) and (partialMatch) == 0:
        return "No matches"
    elif (exactMatch == len(target)):
        return "You win!!!"
    else:
        # report the number of exact matches:
        if (exactMatch == 1):
            exactMatchString = "1 exact match"
        elif (exactMatch > 1):
            exactMatchString = str(exactMatch) + " exact matches"
        # report the number of partial matches:
        if (partialMatch == 1):
            partialMatchString = "1 partial match"
        elif (partialMatch > 1):
            partialMatchString = str(partialMatch) + " partial matches"
        # report only the type(s) of matches that exist:
        if (exactMatch == 0):
            return partialMatchString
        elif (partialMatch == 0):
            return exactMatchString
        else:
            return (exactMatchString + ", " + partialMatchString)

def evalHand(hand):
    return 42

def playPoker(deck, players):
    return 42

# fills in the missing grid entries with lowercase letters starting from z:
def padString(s, rows, cols):
    numToAdd = (rows * cols) - len(s)
    filler = string.ascii_lowercase[::-1]
    s += filler[:numToAdd]
    return s

def testPadString():
    print('Testing padString()...', end='')
    assert(padString("WEATTACKATDAWN", 4, 4) == "WEATTACKATDAWNzy")
    assert(padString("WEATTACKATDAWN", 3, 5) == "WEATTACKATDAWNz") 
    assert(padString("WEATTACKATDAWN", 5, 3) == "WEATTACKATDAWNz") 
    print('Passed!')

# turns a padded string into the conceptual 2d grid:
def gridString(s, rows, cols):
    gridded = ""
    for row in range(rows):
        for col in range(cols):
            i = (rows * col) + row
            gridded += s[i]
    return gridded

def testGridString():
    print('Testing gridString()...', end='')
    assert(gridString("WEATTACKATDAWNzy", 4, 4) == "WTAWEATNACDzTKAy")
    assert(gridString("WEATTACKATDAWNz", 3, 5) == "WTCTWETKDNAAAAz") 
    assert(gridString("WEATTACKATDAWNz", 5, 3) == "WADECAAKWTANTTz") 
    print('Passed!')

# makes every other row of the grid go right-to-left:
def alternateString(s, cols):
    alternated = ""
    for i in range(0, len(s), cols):
        # get each row (len(row) = no. of cols):
        row = s[i:i+cols]
        if ((i // cols) % 2 == 0): 
            alternated += row
        else:
            alternated += row[::-1]
    return alternated

def testAlternateString():
    print('Testing alternateString()...', end='')
    assert(alternateString("WTAWEATNACDzTKAy", 4) == "WTAWNTAEACDzyAKT")
    assert(alternateString("WTCTWETKDNAAAAz", 5) == "WTCTWNDKTEAAAAz") 
    assert(alternateString("WADECAAKWTANTTz", 3) == "WADACEAKWNATTTz") 
    print('Passed!')

# turns a text into a right-left route cipher:
def encodeRightLeftRouteCipher(text, rows):
    cols = math.ceil(len(text)/rows)
    padded = padString(text, rows, cols)
    gridded = gridString(padded, rows, cols)
    alternated = alternateString(gridded, cols)
    return (str(rows) + alternated)

# splits a right-left route cipher into the prefix (rows) and the cipher:
def splitCipher(cipher):
    rowStr = ""
    while (cipher[0].isdigit()):
        rowStr += cipher[0]
        cipher = cipher[1:]
    rows = int(rowStr)
    return (rows, cipher)

def testSplitCipher():
    print('Testing splitCipher()...', end='')
    assert(splitCipher("3WTCTWNDKTEAAAAz") == (3, "WTCTWNDKTEAAAAz"))
    assert(splitCipher("5WADACEAKWNATTTz") == (5, "WADACEAKWNATTTz")) 
    assert(splitCipher("10PCPYFLUZUFFXYYCFEREEBMPTLWAUSC") ==
                       (10, "PCPYFLUZUFFXYYCFEREEBMPTLWAUSC"))
    print('Passed!')

# turns a conceptual 2d grid into a padded string:
def ungridCipher(cipher, cols):
    ungridded = ""
    for col in range(cols):
        for i in range(col, len(cipher), cols):
            ungridded += cipher[i]
    return ungridded

def testUngridCipher():
    print('Testing ungridCipher()...', end='')
    assert(ungridCipher("WTAWEATNACDzTKAy", 4) == "WEATTACKATDAWNzy")
    assert(ungridCipher("WTCTWETKDNAAAAz", 5) == "WEATTACKATDAWNz") 
    assert(ungridCipher("WADECAAKWTANTTz", 3) == "WEATTACKATDAWNz") 
    print('Passed!')

# removes the filler entries of a padded string:
def unpadCipher(s):
    unpadded = ""
    for c in s:
        if (c.isupper()):
            unpadded += c
    return unpadded

def testUnpadCipher():
    print('Testing unpadCipher()...', end='')
    assert(unpadCipher("WEATTACKATDAWNzy") == "WEATTACKATDAWN")
    assert(unpadCipher("WEATTACKATDAWNz") == "WEATTACKATDAWN") 
    assert(unpadCipher("WEATTACKATDAWNz") == "WEATTACKATDAWN") 
    print('Passed!')

# turns a right-left route cipher into paintext:
def decodeRightLeftRouteCipher(cipher):
    (rows, cipher) = splitCipher(cipher)
    cols = len(cipher) // rows
    unalternated = alternateString(cipher, cols)
    ungridded = ungridCipher(unalternated, cols)
    unpadded = unpadCipher(ungridded)
    return unpadded

def topLevelFunctionNames(code):
    return 42

def getNextOperater(expr):
    if ("**" in expr):
        return "**"
    else:
        # look for *, /, // and % first:
        for i in range(len(expr)):
            if (expr[i] == "*") or (expr[i] == "/") or (expr[i] == "%"):
                if (expr[i] == "/") and (expr[i+1] == "/"):
                    operater = "//"
                else:
                    operater = expr[i]
                return operater
        # if no */%, then look for + and -:
        for c in expr:
            if (c == "+") or (c == "-"):
                return c

def testGetNextOperater():
    print('Testing getNextOperater()...', end='')
    assert(getNextOperater("2+3*4-8**3//3") == "**")
    assert(getNextOperater("2+3*4-24//3") == "*") 
    assert(getNextOperater("2+12-24//3") == "//")
    assert(getNextOperater("2+12-8") == "+")
    print('Passed!')

# gets the number before an operater and the expression before it:
def getPrevNumber(expr, operaterIndex):
    prevIndex = operaterIndex - 1
    numStr = ""
    # get all the numbers before hitting another operater:
    while (prevIndex > -1) and (expr[prevIndex].isdigit()):
        numStr = expr[prevIndex] + numStr
        prevIndex -= 1
    prev = expr[:prevIndex+1]
    num = int(numStr)
    return (prev, num)

def testGetPrevNumber():
    print('Testing getPrevNumber()...', end='')
    assert(getPrevNumber("2+3*4-8**3//3", 7) == ("2+3*4-", 8))
    assert(getPrevNumber("2+3*4-24//3", 3) == ("2+", 3)) 
    assert(getPrevNumber("2+12-24//3", 7) == ("2+12-", 24))
    assert(getPrevNumber("2+12-8", 1) == ("", 2))
    print('Passed!')

# gets the number after an operater and the expression after it:
def getNextNumber(expr, operater, operaterIndex):
    if (operater == "**") or (operater == "//"):
        # for ** and //, the number is 1 more index away than other operaters:
        nextIndex = operaterIndex + 2
    else:
        nextIndex = operaterIndex + 1
    numStr = ""
    # get all the numbers before hitting another operater:
    while (nextIndex < len(expr)) and (expr[nextIndex].isdigit()):
        numStr += expr[nextIndex]
        nextIndex += 1
    rest = expr[nextIndex:]
    num = int(numStr)
    return (rest, num)

def testGetNextNumber():
    print('Testing getNextNumber()...', end='')
    assert(getNextNumber("2+3*4-8**3//3", "**", 7) == ("//3", 3))
    assert(getNextNumber("2+3*4-24//3", "*", 3) == ("-24//3", 4))
    assert(getNextNumber("2+12-24//3", "//", 7) == ("", 3))
    assert(getNextNumber("2+12-8", "+", 1) == ("-8", 12))
    print("Passed!")

# returns the expression after applying a single operater:
def applyNextOperater(expr, operater):
    operaterIndex = expr.find(operater)
    (prev, num1) = getPrevNumber(expr, operaterIndex)
    (rest, num2) = getNextNumber(expr, operater, operaterIndex)
    if (operater == "**"):
        result = num1 ** num2
    elif (operater == "*"):
        result = num1 * num2
    elif (operater == "/"):
        result = num1 / numr2
    elif (operater == "//"):
        result = num1 // num2
    elif (operater == "%"):
        result = num1 % num2
    elif (operater == "+"):
        result = num1 + num2
    else:
        result = num1 - num2
    return (prev + str(result) + rest)

def testApplyNextOperater():
    print('Testing applyNextOperater()...', end='')
    assert(applyNextOperater("2+3*4-8**3//3", "**") == "2+3*4-512//3")
    assert(applyNextOperater("2+3*4-24//3", "*") == "2+12-24//3") 
    assert(applyNextOperater("2+12-24//3", "//") == "2+12-8")
    assert(applyNextOperater("2+12-8", "+") == "14-8")
    print('Passed!')

# returns the step-by-step evaluation of an expression:
def getEvalSteps(expr):
    if (expr.isdigit()):
        return (expr + " = " + expr)
    else:
        result = expr
        newLine = "\n" + (" " * len(expr))
        nextStep = expr
        # evaluation proceeds until no operator remains:
        while (not nextStep.isdigit()):
            nextOperater = getNextOperater(nextStep)
            nextStep = applyNextOperater(nextStep, nextOperater)
            result += " = " + nextStep + newLine
        result = result.strip()
        return result

# encodes a msg by shifting the lowercase characters by 1 ascii value:
def bonusEncode1(msg):
    result = ""
    for c in msg:
        if (c.islower()):
            c = chr(ord('a') + (ord(c) - ord('a') + 1)%26)
        result += c
    return result

# decodes a code by shifting the lowercase characters by -1 ascii value:
def funDecode1(code):
    result = ""
    for c in code:
        if (c.islower()):
            c = chr(ord('a') + (ord(c) - ord('a') - 1)%26)
        result += c
    return result

# encodes a msg by shifting each charater according to its index:
def bonusEncode2(msg):
    result = ""
    p = string.ascii_letters + string.digits
    for i in range(len(msg)):
        c = msg[i]
        if (c in p): c = p[(p.find(c) - i) % len(p)]
        result += c
    return result

# decodes a code by shifting each character back according to its index:
def funDecode2(code):
    result = ""
    p = string.ascii_letters + string.digits
    for i in range(len(code)):
        c = code[i]
        if (c in p): c = p[(p.find(c) + i) % len(p)]
        result += c
    return result

# encodes a msg as the difference in ascii value between each character
# and its previous character:
def bonusEncode3(msg):
    result = ""
    prev = 0
    for i in range(len(msg)):
        curr = ord(msg[i])
        if (result != ""): result += ","
        if ((i+1) % 15 == 0): result += "\n"
        result += str(curr - prev)
        prev = curr
    return result

# decodes a code by adding each number to its previous number to get the 
# ascii value of each character:
def funDecode3(code):
    result = ""
    prev = 0
    code = code.strip()
    for numStr in code.split(","):
        curr = int(numStr)
        result += chr(prev + curr)
        prev = prev + curr
    return result

#################################################
# Test Functions
#################################################

def testTopScorer():
    print('Testing topScorer()...', end='')
    data = '''\
Fred,10,20,30,40
Wilma,10,20,30
'''
    assert(topScorer(data) == 'Fred')

    data = '''\
Fred,10,20,30
Wilma,10,20,30,40
'''
    assert(topScorer(data) == 'Wilma')

    data = '''\
Fred,11,20,30
Wilma,10,20,30,1
'''
    assert(topScorer(data) == 'Fred,Wilma')
    assert(topScorer('') == None)
    print('Passed!')

def testWordWrap():
    print('Testing wordWrap()...', end='')
    assert(wordWrap("abc", 3) == "abc")
    assert(wordWrap("abc",2) == "ab\nc") 
    assert(wordWrap("abcdefghij", 4)  ==  """\
abcd
efgh
ij""")
    assert(wordWrap("a b c de fg",  4)  ==  """\
a-b
c-de
fg""")
    print('Passed!')

def testLongestSubpalindrome():
    print("Testing longestSubpalindrome()...", end="")
    assert(longestSubpalindrome("ab-4-be!!!") == "b-4-b")
    assert(longestSubpalindrome("abcbce") == "cbc")
    assert(longestSubpalindrome("aba") == "aba")
    assert(longestSubpalindrome("a") == "a")
    print("Passed!")

def testMastermindScore():
    print("Testing mastermindScore()...", end="")
    assert(mastermindScore('abcd', 'aabd') ==
                           '2 exact matches, 1 partial match')
    assert(mastermindScore('efgh', 'abef') ==
                           '2 partial matches')
    assert(mastermindScore('efgh', 'efef') ==
                           '2 exact matches')
    assert(mastermindScore('ijkl', 'mnop') ==
                           'No matches')
    assert(mastermindScore('cdef', 'cccc') ==
                           '1 exact match')
    assert(mastermindScore('cdef', 'bccc') ==
                           '1 partial match')
    assert(mastermindScore('wxyz', 'wwwx') ==
                           '1 exact match, 1 partial match')
    assert(mastermindScore('wxyz', 'wxya') ==
                           '3 exact matches')
    assert(mastermindScore('wxyz', 'awxy') ==
                           '3 partial matches')
    assert(mastermindScore('wxyz', 'wxyz') ==
                           'You win!!!')
    print("Passed!'")

def testPlayPoker():
    print('Testing playPoker()...', end='')
    assert(playPoker('QD-3S', 1) == 'Player 1 wins with a high card of QD')
    assert(playPoker('QD-QC', 1) == 'Player 1 wins with a pair to QD')
    assert(playPoker('QD-JS', 1) == 'Player 1 wins with a straight to QD')
    assert(playPoker('TD-QD', 1) == 'Player 1 wins with a flush to QD')
    assert(playPoker('QD-JD', 1) == 'Player 1 wins with a straight flush to QD')
    assert(playPoker('QD-JD', 2) == 'Not enough cards')

    assert(playPoker('AS-2H-3C-4D', 2) ==
                                    'Player 2 wins with a high card of 4D')
    assert(playPoker('5S-2H-3C-4D', 2) ==
                                    'Player 1 wins with a high card of 5S')
    assert(playPoker('AS-2H-3C-2D', 2) == 'Player 2 wins with a pair to 2H')
    assert(playPoker('3S-2H-3C-2D', 2) == 'Player 1 wins with a pair to 3S')
    assert(playPoker('AS-2H-2C-2D', 2) == 'Player 1 wins with a straight to 2C')
    assert(playPoker('AS-2H-2C-3D', 2) == 'Player 2 wins with a straight to 3D')
    assert(playPoker('AS-2H-4S-3D', 2) == 'Player 1 wins with a flush to 4S')
    assert(playPoker('AS-2H-4S-3H', 2) ==
                                    'Player 2 wins with a straight flush to 3H')
    assert(playPoker('2S-2H-3S-3H', 2) ==
                                    'Player 1 wins with a straight flush to 3S')

    assert(playPoker('AS-2D-3C-4C-5H-6D-7S-8D', 2) ==
                                    'Player 2 wins with a high card of 4C')
    assert(playPoker('AS-2D-3S-4C-5H-6D-7S-8D', 4) ==
                                    'Player 3 wins with a flush to 7S')
    print('Passed!')

def testEncodeRightLeftRouteCipher():
    print('Testing encodeRightLeftRouteCipher()...', end='')
    assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",4) ==
                                      "4WTAWNTAEACDzyAKT")
    assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",3) ==
                                      "3WTCTWNDKTEAAAAz") 
    assert(encodeRightLeftRouteCipher("WEATTACKATDAWN",5) ==
                                      "5WADACEAKWNATTTz") 
    assert(encodeRightLeftRouteCipher("PLUXYRETLCCFZFYEEPWSPYUFCFBMAU",10) ==
                                      "10PCPYFLUZUFFXYYCFEREEBMPTLWAUSC") 
    print('Passed!')

def testDecodeRightLeftRouteCipher():
    print('Testing decodeRightLeftRouteCipher()...', end='')
    assert(decodeRightLeftRouteCipher("4WTAWNTAEACDzyAKT") ==
                                      "WEATTACKATDAWN")
    assert(decodeRightLeftRouteCipher("3WTCTWNDKTEAAAAz") ==
                                      "WEATTACKATDAWN") 
    assert(decodeRightLeftRouteCipher("5WADACEAKWNATTTz") ==
                                      "WEATTACKATDAWN") 
    assert(decodeRightLeftRouteCipher("10PCPYFLUZUFFXYYCFEREEBMPTLWAUSC") ==
                                      "PLUXYRETLCCFZFYEEPWSPYUFCFBMAU")
    text = "WEATTACKATDAWN"
    cipher = encodeRightLeftRouteCipher(text, 6)
    plaintext = decodeRightLeftRouteCipher(cipher)
    assert(plaintext == text)
    print('Passed!')

def testEncodeAndDecodeRightLeftRouteCipher():
    testEncodeRightLeftRouteCipher()
    testDecodeRightLeftRouteCipher()

def testTopLevelFunctionNames():
    print("Testing topLevelFunctionNames()...", end="")

    # no fn defined
    code = """\
# This has no functions!
# def f(): pass
print("Hello world!")
"""
    assert(topLevelFunctionNames(code) == "")

    # f is redefined
    code = """\
def f(x): return x+42
def g(x): return x+f(x)
def f(x): return x-42
"""
    assert(topLevelFunctionNames(code) == "f.g")

    # def not at start of line
    code = """\
def f(): return "def g(): pass"
"""
    assert(topLevelFunctionNames(code) == "f")

    # g() is in triple-quotes (''')
    code = """\
def f(): return '''
def g(): pass'''
"""
    assert(topLevelFunctionNames(code) == "f")

    # g() is in triple-quotes (""")
    code = '''\
def f(): return """
def g(): pass"""
'''
    assert(topLevelFunctionNames(code) == "f")

    # triple-quote (''') in comment
    code = """\
def f(): return 42 # '''
def g(): pass # '''
"""
    assert(topLevelFunctionNames(code) == "f.g")

    # triple-quote (""") in comment
    code = '''\
def f(): return 42 # """
def g(): pass # """
'''
    assert(topLevelFunctionNames(code) == "f.g")

    # comment character (#) in quotes
    code = """\
def f(): return '#' + '''
def g(): pass # '''
def h(): return "#" + '''
def i(): pass # '''
def j(): return '''#''' + '''
def k(): pass # '''
"""
    assert(topLevelFunctionNames(code) == "f.h.j")
    print("Passed!")

def testGetEvalSteps():
    print("Testing getEvalSteps()...", end="")
    assert(getEvalSteps("0") == "0 = 0")
    assert(getEvalSteps("2") == "2 = 2")
    assert(getEvalSteps("3+2") == "3+2 = 5")
    assert(getEvalSteps("3-2") == "3-2 = 1")
    assert(getEvalSteps("3**2") == "3**2 = 9")
    assert(getEvalSteps("31%16") == "31%16 = 15")
    assert(getEvalSteps("31*16") == "31*16 = 496")
    assert(getEvalSteps("32//16") == "32//16 = 2")
    assert(getEvalSteps("2+3*4") == "2+3*4 = 2+12\n      = 14")
    assert(getEvalSteps("2*3+4") == "2*3+4 = 6+4\n      = 10")
    assert(getEvalSteps("2+3*4-8**3%3") == """\
2+3*4-8**3%3 = 2+3*4-512%3
             = 2+12-512%3
             = 2+12-2
             = 14-2
             = 12""")
    assert(getEvalSteps("2+3**4%2**4+15//3-8") == """\
2+3**4%2**4+15//3-8 = 2+81%2**4+15//3-8
                    = 2+81%16+15//3-8
                    = 2+1+15//3-8
                    = 2+1+5-8
                    = 3+5-8
                    = 8-8
                    = 0""")
    print("Passed!")

def testFunDecoder(encodeFn, decodeFn):
    s1 = ''
    for c in range(15):
        if (random.random() < 0.80):
            s1 += random.choice(string.ascii_letters)
        else:
            s1 += random.choice(' \n\n') + random.choice(string.digits)
    for s in ['a', 'abc', s1]:
        if (decodeFn(encodeFn(s)) != s):
            raise Exception(f'Error in {decodeFn.__name__} on {repr(s)}')
    return True

def testFunDecoders():
    print('Testing funDecoders()...', end='')
    testFunDecoder(bonusEncode1, funDecode1)
    testFunDecoder(bonusEncode2, funDecode2)
    testFunDecoder(bonusEncode3, funDecode3)
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    # required
    testTopScorer()

    # mild
    testWordWrap()
    #testLongestSubpalindrome()

    # medium
    testGetMatches()
    testMastermindScore()
    #testPlayPoker()

    # spicy
    testPadString()
    testGridString()
    testAlternateString()
    testSplitCipher()
    testUngridCipher()
    testUnpadCipher()
    testEncodeAndDecodeRightLeftRouteCipher()
    #testTopLevelFunctionNames()
    testGetNextOperater()
    testGetPrevNumber()
    testGetNextNumber()
    testApplyNextOperater()
    testGetEvalSteps()
    testFunDecoders()

def main():
    cs112_s20_unit3_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
