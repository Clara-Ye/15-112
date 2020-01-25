#################################################
# hw2.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_s20_unit2_linter
import basic_graphics
import math

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

def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

#################################################
# Functions for you to write
#################################################

# from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors:
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def drawFancyWheel(canvas, cx, cy, r, n, color):
    # draw the circle:
    canvas.create_oval((cx - r), (cy - r), (cx + r), (cy + r), outline = color)
    # draw the lines:
    for startPoint in range(n):
        angleStartPoint = (math.pi/2) - (((math.pi*2) * startPoint) / n)
        startPointX = roundHalfUp(cx + (r * math.cos(angleStartPoint)))
        startPointY = roundHalfUp(cy - (r * math.sin(angleStartPoint)))
        for endPoint in range((startPoint + 1), n):
            angleEndPoint = (math.pi/2) - (((math.pi*2) * endPoint) / n)
            endPointX = roundHalfUp(cx + (r * math.cos(angleEndPoint)))
            endPointY = roundHalfUp(cy - (r * math.sin(angleEndPoint)))
            canvas.create_line(startPointX, startPointY, endPointX, endPointY,
                               fill = color)

def drawFancyWheels(canvas, width, height, rows, cols):
    # find the radius:
    cellWidth = width // cols
    cellHeight = height // rows
    radius = ((min(cellWidth, cellHeight)) / 2) * 0.9
    # blue is always 0:
    blue = 0
    for row in range(rows):
        # red and cy depend on the row:
        red = row * roundHalfUp(255 / rows)
        cy = (cellHeight // 2) + (cellHeight * row)
        for col in range(cols):
            # green and cx depend on the column:
            green = 255 - (col * roundHalfUp(255 / cols))
            cx = (cellWidth // 2) + (cellWidth * col)
            # points and color depend on both row and column:
            points = 4 + row + col
            color = rgbString(red, green, blue)
            # call drawFancyWheel():
            drawFancyWheel(canvas, cx, cy, radius, points, color)
    return None

def mostFrequentDigit(n):
    n = abs(n)
    maxFrequency = -1
    mostFrequent = None
    for digit in range(10):
        count = 0
        number = n
        while number > 0:
            if ((number % 10) == digit):
                count += 1
            number //= 10
        if (count > maxFrequency):
            maxFrequency = count
            mostFrequent = digit
    return mostFrequent

# from https://www.cs.cmu.edu/~112/notes/notes-loops.html#isPrime:
def isPrime(n):
    if (n < 2):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    maxFactor = roundHalfUp(n**0.5)
    for factor in range(3, maxFactor+1, 2):
        if (n % factor == 0):
            return False
    return True

def digitCount(n):
    n = abs(n)
    count = 1
    while (n > 10):
        n //= 10
        count += 1
    return count

def getKthDigit(n, k):
    n = abs(n)
    return (n // (10**k) % 10)

def isPalindromic(n):
    if (n < 10):
        return True
    else:
        digit = 0
        totalDigits = digitCount(n)
        # need to check until the middle of the number:
        for digit in range(math.ceil(totalDigits / 2)):
            firstDigit = getKthDigit(n, digit)
            lastDigit = getKthDigit(n, (totalDigits - digit - 1))
            if (firstDigit != lastDigit):
                return False
        # return True only if all digits pair up:
        return True

def nthPalindromicPrime(n):
    guess = 0
    count = 0
    while (count <= n):
        guess += 1
        if isPrime(guess):
            if isPalindromic(guess):
                count += 1
    return guess

def carrylessAdd(x, y):
    total = 0
    digit = 0
    while (x > 0) or (y > 0):
        # get the first digits:
        onesX = x % 10
        onesY = y % 10
        # add the first digits, only keep the first digit of the sum:
        tempSum = (onesX + onesY) % 10
        # add this digit to the corresponding digit of the total sum:
        total += tempSum * (10 ** digit)
        # move on to the next digit
        x //= 10
        y //= 10
        digit += 1
    return total

def integral(f, a, b, N):
    trapezoidWidth = (b - a) / N
    totalArea = 0
    for n in range(N):
        leftHeight = f(a + (n * trapezoidWidth))
        rightHeight = f(a + ((n + 1) * trapezoidWidth))
        area = ((leftHeight + rightHeight) * trapezoidWidth) / 2
        totalArea += area
    return totalArea

def hasDigit(n, digit):
    while (n > 0):
        ones = n % 10
        n //= 10
        if (digit == ones):
            return True
    return False

def isWithProperty309(n):
    powered = n ** 5
    for number in range(10):
        if (hasDigit(powered, number) == False):
            return False
    return True

def nthWithProperty309(n):
    guess = 309
    count = 0
    while (count < n):
        guess += 1
        if isWithProperty309(guess):
            count += 1
    return guess

def rotateDigits(n):
    ones = n % 10
    rest = n // 10
    totalDigits = digitCount(n)
    rotation = ones * (10 ** (totalDigits - 1)) + rest
    return rotation
    
def isCircularPrime(n):
    # needs to be a prime:
    if (isPrime(n) == False):
        return False
    # one-digit numbers are circular, so only check if is prime:
    elif (n < 10):
        return isPrime(n)
    else:
        # check if each rotation of digits is prime:
        totalDigits = digitCount(n)
        for digit in range(1, totalDigits):
            n = rotateDigits(n)
            if (isPrime(n) == False):
                return False
        return True

def nthCircularPrime(n):
    guess = 2
    count = 0
    while (count < n):
        guess += 1
        if isCircularPrime(guess):
            count += 1
    return guess

def findZeroWithBisection(f, x0, x1, epsilon):
    if (f(x0) * f(x1) > 0):
        return None
    xMid = (x0 + x1) / 2
    while almostEqual(f(xMid), 0, epsilon) == False:
        # check the half with change of sign in the next loop:
        if (f(x0) * f(xMid) < 0):
            x1 = xMid
        else:
            x0 = xMid
        xMid = (x0 + x1) / 2
    return xMid

def sumDigits(n):
    total = 0
    while (n > 0):
        ones = n % 10
        total += ones
        n //= 10
    return total

def sumFactor(n):
    if isPrime(n):
        return 0
    else:
        factor = 2
        total = 0
        while (n > 1):
            # add factor to sum whenever found one
            if (n % factor == 0):
                n //= factor
                total += sumDigits(factor)
            # or continue to look for factors
            else:
                factor += 1
        return total
            
def nthSmithNumber(n):
    guess = 4
    count = 0
    while (count < n):
        guess += 1
        if (sumDigits(guess) == sumFactor(guess)):
            count += 1
    return guess

def carrylessMultiply(x1, x2):
    digit = 0
    total = 0
    while (x2 > 0):
        ones = x2 % 10
        tempSum = 0
        # carrylessly add x1 ones times:
        while (ones > 0):
            tempSum = carrylessAdd(tempSum, x1)
            ones -= 1
        # add this digit to the corresponding digit of the total sum:
        total = carrylessAdd(total, (tempSum * (10**digit)))
        # move on to the next digit:
        digit += 1
        x2 //= 10
    return total

def isKaprekarNumber(n):
    if isinstance(n, int) == False:
        return False
    elif (n == 1):
        return True
    else:
        powered = n**2
        left = powered
        totalDigits = digitCount(powered)
        # break the number at each digit and add them up:
        for digit in range(1, totalDigits):
            left = powered // (10**digit)
            right = powered % (10**digit)
            if (left + right == n) and (right != 0):
                return True
        return False

def nthKaprekarNumber(n):
    guess = 1
    count = 0
    while (count < n):
        guess += 1
        if isKaprekarNumber(guess):
            count += 1
    return guess

def nthCarolPrime(n):
    # 0th Carol Prime is 7, when k = 3:
    k = 3
    guess = 7
    count = 0
    # check if each Carol number is prime:
    while (count < n):
        guess = ((((2**k) - 1)**2) - 2)
        if isPrime(guess):
            count += 1
        k += 1
    return guess

def makeBoard(moves):
    board = 0
    while (moves > 0):
        board += 8 * (10**(moves - 1))
        moves -= 1
    return board

def kthDigit(n, k):
    return getKthDigit(n, k)

def replaceKthDigit(n,k,d):
    absN = abs(n)
    kthD = kthDigit(n, k)
    newNum = absN - (kthD * (10**k)) + (d * (10**k))
    if (n >= 0):
        return newNum
    else:
        return (newNum * -1)

def getLeftmostDigit(n):
    leftmost = digitCount(n) - 1
    leftmostDigit = kthDigit(n, leftmost)
    return leftmostDigit

def clearLeftmostDigit(n):
    leftmost = digitCount(n) - 1
    cleared = replaceKthDigit(n, leftmost, 0)
    return cleared

def makeMove(board, position, move):
    if (move != 1) and (move != 2):
        return "move must be 1 or 2!"
    else:
        numOfPosition = digitCount(board)
        if (numOfPosition < position):
            return "offboard!"
        elif (kthDigit(board, (numOfPosition - position)) != 8):
            return "occupied!"
        else:
            return replaceKthDigit(board, (numOfPosition - position), move)

def isWin(board):
    while (board > 0):
        ones = board % 10
        tens = (board // 10) % 10
        # look for 112 if see a 12:
        if (ones == 2) and (tens == 1):
            hundreds = (board // 100) % 10
            # win if see 112:
            if (hundreds == 1):
                return True
        board //= 10
    return False

def isFull(board):
    while (board > 0):
        ones = board % 10
        if (ones == 8):
            return False
        board //= 10
    return True

def play112(game):
    # initialize the board:
    size = getLeftmostDigit(game)
    board = makeBoard(size)
    game = clearLeftmostDigit(game)
    turn = 1
    while (game > 0):
        # play the game:
        position = size - getLeftmostDigit(game)
        if (position < 0):
            return (str(board) + ": Player " + str(turn) + ": offboard!")
        if (kthDigit(board, position) != 8):
            return (str(board) + ": Player " + str(turn) + ": occupied!")
        game = clearLeftmostDigit(game)
        move = getLeftmostDigit(game)
        if (move != 1) and (move!= 2):
            return (str(board)+": Player "+str(turn)+": move must be 1 or 2!")
        board = replaceKthDigit(board, position, move)
        # check winning results:
        if isWin(board):
            return (str(board) + ": Player " + str(turn) + " wins!")
        elif isFull(board):
            return (str(board) + ": Tie!")
        else:
            if (turn == 1):
                turn = 2
            else:
                turn = 1
            game = clearLeftmostDigit(game)
    return (str(board) + ": Unfinished!")

############################
# integerDataStructures
# If you do this spicy problem,
# place your solutions here!
############################

# take two non-negative integers and return their concatenation
def intCat(n, m):
    digitM = digitCount(m)
    return ((n * (10**digitM)) + m)

def lengthEncode(n):
    # get the sign:
    if (n >= 0):
        sign = 1
    else:
        sign = 2
    n = abs(n)
    # include the count:
    count = digitCount(n)
    code = intCat(count, n)
    # include the count-count:
    countCount = digitCount(count)
    code = intCat(countCount, code)
    # include the sign:
    code = intCat(sign, code)
    return code

def getPrefix(n):
    length = digitCount(n)
    sign = getKthDigit(n, (length - 1))
    countCount = getKthDigit(n, (length - 2))
    count = 0
    for digit in range(countCount):
        nextDigit = getKthDigit(n, (length - 3 - digit))
        count = intCat(count, nextDigit)
    return (sign, countCount, count)

def lengthDecode(n):
    (sign, countCount, count) = getPrefix(n)
    number = n % (10**(count))
    # add sign to number:
    if (sign == 1):
        return number
    else:
        return -number

def getLeftmostCode(n):
    (sign, countCount, count) = getPrefix(n)
    # get the lengths of the leftmost value and the rest:
    lengthTotal = digitCount(n)
    lengthLeftmostCode = countCount + count + 2
    lengthRest = lengthTotal - lengthLeftmostCode
    # split n into leftmost value and the rest:
    leftmostCode = n // (10**(lengthRest))
    rest = n % (10**(lengthRest))
    return (leftmostCode, rest)

def lengthDecodeLeftmostValue(n):
    (leftmostCode, rest) = getLeftmostCode(n)
    leftmostValue = lengthDecode(leftmostCode)
    return (leftmostValue, rest)

def newIntList():
    return lengthEncode(0)

def intListLen(L):
    (lengthCode, elementCode) = getLeftmostCode(L)
    lengthValue = lengthDecode(lengthCode)
    return lengthValue

def intListGet(L, i):
    lengthList = intListLen(L)
    if (i >= lengthList):
        return "index out of range"
    else:
        (leftmostValue, rest) = lengthDecodeLeftmostValue(L)
        for index in range(i+1):
            (leftmostValue, rest) = lengthDecodeLeftmostValue(rest)
        return leftmostValue

def intListSet(L, i, v):
    lengthList = intListLen(L)
    if (i >= lengthList):
        return "index out of range"
    else:
        # split L into left, mid (to replace), and right:
        left = 0
        rest = L
        for index in range(i+1):
            (leftmostCode, rest) = getLeftmostCode(rest)
            left = intCat(left, leftmostCode)
        (mid, right) = getLeftmostCode(rest)
        # replace mid with the new code:
        newCode = lengthEncode(v)
        newL = intCat(left, newCode)
        # to avoid appending an extra 0:
        if (right != 0):
            newL = intCat(newL, right)
    return newL

def intListAppend(L, v):
    # calculate new list length:
    (listLength, listElements) = getLeftmostCode(L)
    newListLengthValue = intListLen(L) + 1
    newListLengthCode = lengthEncode(newListLengthValue)
    # change list length while avoiding an extra 0:
    if (listElements != 0):
        newL = intCat(newListLengthCode, listElements)
    else:
        newL = newListLengthCode
    # append the new value
    newCode = lengthEncode(v)
    newL = intCat(newL, newCode)
    return newL

def intListPop(L):
    # calculate new list length:
    (listLength, listElements) = getLeftmostCode(L)
    newListLengthValue = intListLen(L) - 1
    newListLengthCode = lengthEncode(newListLengthValue)
    # add each element but the last after the list length
    left = newListLengthCode
    poppedCode = listElements
    for index in range(newListLengthValue):
        (leftmostCode, poppedCode) = getLeftmostCode(poppedCode)
        left = intCat(left, leftmostCode)
    # decode the last (popped) value
    poppedValue = lengthDecode(poppedCode)
    return (left, poppedValue)

def newIntSet():
    return lengthEncode(0)

def intSetAdd(s, v):
    if intSetContains(s, v):
        return s
    else:
        newS = intListAppend(s, v)
        return newS

def intSetContains(s, v):
    vCode = lengthEncode(v)
    (setLengthCode, rest) = getLeftmostCode(s)
    while (rest != 0):
        (toCheck, rest) = getLeftmostCode(rest)
        if (toCheck == vCode):
            return True
    return False

def newIntMap():
    return lengthEncode(0)

def intMapContains(m, key):
    return intSetContains(m, key)

def intMapFind(m, element):
    code = lengthEncode(element)
    (mapLengthCode, rest) = getLeftmostCode(m)
    mapLength = lengthDecode(mapLengthCode)
    while (rest != 0):
        (toCheck, rest) = getLeftmostCode(rest)
        if (toCheck == code):
            return rest

def intMapGet(m, key):
    if intMapContains(m, key):
        rest = intMapFind(m, key)
        (value, rest) = lengthDecodeLeftmostValue(rest)
        return value
    else:
        return "no such key"

def intMapSet(m, key, value):
    if intMapContains(m, key):
        rest = intMapFind(m, key)
        left = m // (10 ** digitCount(rest)) 
        (toReplace, right) = getLeftmostCode(rest)
        valueCode = lengthEncode(value)
        newMap = intCat(left, valueCode)
        if (right != 0):
            newMap = intCat(newMap, right)
    else:
        newMap = intListAppend(m, key)
        newMap = intListAppend(newMap, value)
    return newMap

def newIntFSM():
    emptyList = newIntList()
    emptyMap = newIntMap()
    emptySet = newIntSet()
    fsm = intListAppend(emptyList, emptyMap)
    fsm = intListAppend(fsm, emptySet)
    return fsm

# splits a fsm into a map and a set
def intFSMSplit(fsm):
    (lengthCode, rest) = getLeftmostCode(fsm)
    (stateMapCode, stateSetCode) = getLeftmostCode(rest)
    return (lengthCode, stateMapCode, stateSetCode)

def isAcceptingState(fsm, state):
    (lengthCode, stateMapCode, stateSetCode) = intFSMSplit(fsm)
    stateSet = lengthDecode(stateSetCode)
    return intSetContains(stateSet, state)

def addAcceptingState(fsm, state):
    # get the decoded set:
    (lengthCode, stateMapCode, stateSetCode) = intFSMSplit(fsm)
    stateSet = lengthDecode(stateSetCode)
    # append state and encode:
    newStateSet = intListAppend(stateSet, state)
    newStateSetCode = lengthEncode(newStateSet)
    # add all the pieces together:
    newFSM = intCat(lengthCode, stateMapCode)
    newFSM = intCat(newFSM, newStateSetCode)
    return newFSM

def setTransition(fsm, fromState, digit, toState):
    # get the decoded map:
    (lengthCode, stateMapCode, stateSetCode) = intFSMSplit(fsm)
    stateMap = lengthDecode(stateMapCode)
    # add the transition to the map:
    newInnerMap = intMapSet(newIntMap(), digit, toState)
    # if the start state is already in the map,
    # turn the value to a list of the existing inner map and the new inner map:
    if intMapContains(stateMap, fromState):
        existingInnerMap = intMapGet(stateMap, fromState)
        innerMapList = intListAppend(newIntList(), existingInnerMap)
        innerMapList = intListAppend(innerMapList, newInnerMap)
        outerMap = intMapSet(stateMap, fromState, innerMapList)
    # otherwise make a new map
    else:
        outerMap = intMapSet(stateMap, fromState, newInnerMap)
    newStateMapCode = lengthEncode(outerMap)
    # add all pieces together:
    newFSM = intCat(lengthCode, newStateMapCode)
    newFSM = intCat(newFSM, stateSetCode)
    return newFSM

def getTransition(fsm, fromState, digit):
    (lengthCode, stateMapCode, stateSetCode) = intFSMSplit(fsm)
    stateMap = lengthDecode(stateMapCode)
    if intMapContains(stateMap, fromState):
        innerMap = intMapGet(stateMap, fromState)
        # if innerMap has 12 digits,
        # it is a regular inner map:
        if (digitCount(innerMap) == 12):
            if intMapContains(innerMap, digit):
                toState = intMapGet(innerMap, digit)
                return toState
        # otherwise it is a list of inner maps:
        else:
            (listLength, rest) = getLeftmostCode(innerMap)
            while (rest != 0):
                (innerMapCode, rest) = getLeftmostCode(rest)
                innerMap = lengthDecode(innerMapCode)
                if intMapContains(innerMap, digit):
                    toState = intMapGet(innerMap, digit)
                    return toState
    return "no such transition"

def accepts(fsm, inputValue):
    digit = digitCount(inputValue) - 1
    fromState = 1
    while (digit >= 0):
        symbol = getKthDigit(inputValue, digit)
        toState = getTransition(fsm, fromState, symbol)
        if (isinstance(toState, int) == False):
            return False
        else:
            fromState = toState
            digit -= 1
    return isAcceptingState(fsm, fromState)

def states(fsm, inputValue):
    visited = intListAppend(newIntList(), 1)
    digit = digitCount(inputValue) - 1
    fromState = 1
    while (digit >= 0):
        symbol = getKthDigit(inputValue, digit)
        toState = getTransition(fsm, fromState, symbol)
        if (isinstance(toState, int) == False):
            return visited
        else:
            visited = intListAppend(visited, toState)
            fromState = toState
            digit -= 1
    return visited

def encodeString(s):
    encodedList = newIntList()
    for c in s:
        number = ord(c)
        encodedList = intListAppend(encodedList, number)
    return encodedList

def decodeString(L):
    message = ""
    (lengthCode, rest) = getLeftmostCode(L)
    while (rest > 0):
        (code, rest) = getLeftmostCode(rest)
        number = lengthDecode(code)
        character = chr(number)
        message += character
    return message

#################################################
# Test Functions
# ignore_rest (tell autograder to ignore everything below here)
#################################################

def testDrawFancyWheels():
    print('Testing drawFancyWheels()... (confirm visually)')
    print('  drawFancyWheels: 1 row x 1 col, win size of 400x400...', end='')
    basic_graphics.run(1, 1, width=400, height=400, drawFn=drawFancyWheels)
    print('  drawFancyWheels: 4 rows x 6 cols, win size of 900x600...', end='')
    basic_graphics.run(4, 6, width=900, height=600, drawFn=drawFancyWheels)

def testMostFrequentDigit():
    print('Testing mostFrequentDigit()...', end='')
    assert mostFrequentDigit(0) == 0
    assert mostFrequentDigit(1223) == 2
    assert mostFrequentDigit(12233) == 2
    assert mostFrequentDigit(-12233) == 2
    assert mostFrequentDigit(1223322332) == 2
    assert mostFrequentDigit(123456789) == 1
    assert mostFrequentDigit(1234567789) == 7
    assert mostFrequentDigit(1000123456789) == 0
    print('Passed.')

def testNthPalindromicPrime():
    print('Testing nthPalindromicPrime()...', end='')
    assert nthPalindromicPrime(0) == 2
    assert nthPalindromicPrime(4) == 11
    assert nthPalindromicPrime(10) == 313
    assert nthPalindromicPrime(15) == 757
    assert nthPalindromicPrime(20) == 10301
    print('Passed.')

def testCarrylessAdd():
    print('Testing carrylessAdd()... ', end='')
    assert(carrylessAdd(785, 376) == 51)
    assert(carrylessAdd(0, 376) == 376)
    assert(carrylessAdd(785, 0) == 785)
    assert(carrylessAdd(30, 376) == 306)
    assert(carrylessAdd(785, 30) == 715)
    assert(carrylessAdd(12345678900, 38984034003) == 40229602903)
    print('Passed.')

def f1(x): return 42
def i1(x): return 42*x 
def f2(x): return 2*x  + 1
def i2(x): return x**2 + x
def f3(x): return 9*x**2
def i3(x): return 3*x**3
def f4(x): return math.cos(x)
def i4(x): return math.sin(x)
def testIntegral():
    print('Testing integral()...', end='')
    epsilon = 10**-4
    assert(almostEqual(integral(f1, -5, +5, 1), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f1, -5, +5, 10), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 1), 4,
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 250), (i2(2)-i2(1)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f3, 4, 5, 250), (i3(5)-i3(4)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f4, 1, 2, 250), (i4(2)-i4(1)),
                      epsilon=epsilon))
    print("Passed!")

def testNthWithProperty309():
    print('Testing nthWithProperty309()... ', end='')
    assert(nthWithProperty309(0) == 309)
    assert(nthWithProperty309(1) == 418)
    assert(nthWithProperty309(2) == 462)
    assert(nthWithProperty309(3) == 474)
    print("Passed!")

def testNthCircularPrime():
    print('Testing nthCircularPrime()...', end='')
    # [2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, 97, 113,
    #  131, 197, 199, 311, 337, 373, 719, 733, 919, 971, 991, 1193, ...]
    assert(nthCircularPrime(0) == 2)
    assert(nthCircularPrime(5) == 13)
    assert(nthCircularPrime(10) == 73)
    assert(nthCircularPrime(15) == 197)
    assert(nthCircularPrime(20) == 719)
    assert(nthCircularPrime(25) == 1193)
    print('Passed!')

def testFindZeroWithBisection():
    print('Testing findZeroWithBisection()... ', end='')
    def f1(x): return x*x - 2 # root at x=sqrt(2)
    x = findZeroWithBisection(f1, 0, 2, 0.000000001)
    assert(almostEqual(x, 1.41421356192))   
    def f2(x): return x**2 - (x + 1)  # root at x=phi
    x = findZeroWithBisection(f2, 0, 2, 0.000000001)
    assert(almostEqual(x, 1.61803398887))
    def f3(x): return x**5 - 2**x # f(1)<0, f(2)>0
    x = findZeroWithBisection(f3, 1, 2, 0.000000001)
    assert(almostEqual(x, 1.17727855081))
    print('Passed.')

def testNthSmithNumber():
    print('Testing nthSmithNumber()... ', end='')
    assert(nthSmithNumber(0) == 4)
    assert(nthSmithNumber(1) == 22)
    assert(nthSmithNumber(2) == 27)
    assert(nthSmithNumber(3) == 58)
    assert(nthSmithNumber(4) == 85)
    assert(nthSmithNumber(5) == 94)
    print('Passed.')

def testCarrylessMultiply():
    print("Testing carrylessMultiply()...", end="")
    assert(carrylessMultiply(643, 59) == 417)
    assert(carrylessMultiply(6412, 387) == 807234)
    print("Passed!")

def testNthKaprekarNumber():
    print('Testing nthKaprekarNumber()...', end='')
    assert(nthKaprekarNumber(0) == 1)
    assert(nthKaprekarNumber(1) == 9)
    assert(nthKaprekarNumber(2) == 45)
    assert(nthKaprekarNumber(3) == 55)
    assert(nthKaprekarNumber(4) == 99)
    assert(nthKaprekarNumber(5) == 297)
    assert(nthKaprekarNumber(6) == 703)
    assert(nthKaprekarNumber(7) == 999)
    print('Passed.')

def testNthCarolPrime():
    print("Testing nthCarolPrime()...", end='')
    assert(nthCarolPrime(0) == 7)
    assert(nthCarolPrime(1) == 47)
    assert(nthCarolPrime(2) == 223)
    assert(nthCarolPrime(3) == 3967)
    assert(nthCarolPrime(6) == 16769023)
    assert(nthCarolPrime(8) == 68718952447)
    assert(nthCarolPrime(9) == 274876858367)
    print("Passed!")

def testPlay112():
    print("Testing play112()... ", end="")
    assert(play112( 5 ) == "88888: Unfinished!")
    assert(play112( 521 ) == "81888: Unfinished!")
    assert(play112( 52112 ) == "21888: Unfinished!")
    assert(play112( 5211231 ) == "21188: Unfinished!")
    assert(play112( 521123142 ) == "21128: Player 2 wins!")
    assert(play112( 521123151 ) == "21181: Unfinished!")
    assert(play112( 52112315142 ) == "21121: Player 1 wins!")
    assert(play112( 523 ) == "88888: Player 1: move must be 1 or 2!")
    assert(play112( 51223 ) == "28888: Player 2: move must be 1 or 2!")
    assert(play112( 51211 ) == "28888: Player 2: occupied!")
    assert(play112( 5122221 ) == "22888: Player 1: occupied!")
    assert(play112( 51261 ) == "28888: Player 2: offboard!")
    assert(play112( 51122324152 ) == "12212: Tie!")
    print("Passed!")

def testLengthEncode():
    print('Testing lengthEncode()...', end='')
    assert(lengthEncode(789) == 113789)
    assert(lengthEncode(-789) == 213789)
    assert(lengthEncode(1234512345) == 12101234512345)
    assert(lengthEncode(-1234512345) == 22101234512345)
    assert(lengthEncode(0) == 1110)
    print('Passed!')

def testLengthDecode():
    print('Testing lengthDecode()...', end='')
    assert(lengthDecode(113789) == 789)
    assert(lengthDecode(213789) == -789)
    assert(lengthDecode(12101234512345) == 1234512345)
    assert(lengthDecode(22101234512345) == -1234512345)
    assert(lengthDecode(1110) == 0)
    print('Passed!')

def testLengthDecodeLeftmostValue():
    print('Testing lengthDecodeLeftmostValue()...', end='')
    assert(lengthDecodeLeftmostValue(111211131114) == (2, 11131114))
    assert(lengthDecodeLeftmostValue(112341115) == (34, 1115))
    assert(lengthDecodeLeftmostValue(111211101110) == (2, 11101110))
    assert(lengthDecodeLeftmostValue(11101110) == (0, 1110))
    print('Passed!')

def testIntList():
    print('Testing intList functions...', end='')
    a1 = newIntList()
    assert(a1 == 1110) # length-encoded 0
    assert(intListLen(a1) == 0)
    assert(intListGet(a1, 0) == 'index out of range')

    a1 = intListAppend(a1, 42)
    assert(a1 == 111111242) # [1, 42]
    assert(intListLen(a1) == 1)
    assert(intListGet(a1, 0) == 42)
    assert(intListGet(a1, 1) == 'index out of range')
    assert(intListSet(a1, 1, 99) == 'index out of range')

    a1 = intListSet(a1, 0, 567)
    assert(a1 == 1111113567) # [1, 567]
    assert(intListLen(a1) == 1)
    assert(intListGet(a1, 0) == 567)

    a1 = intListAppend(a1, 8888)
    a1 = intListSet(a1, 0, 9)
    assert(a1 == 111211191148888) # [1, 9, 8888]
    assert(intListLen(a1) == 2)
    assert(intListGet(a1, 0) == 9)
    assert(intListGet(a1, 1) == 8888)

    a1, poppedValue = intListPop(a1)
    assert(poppedValue == 8888)
    assert(a1 == 11111119) # [1, 9]
    assert(intListLen(a1) == 1)
    assert(intListGet(a1, 0) == 9)
    assert(intListGet(a1, 1) == 'index out of range')

    a2 = newIntList()
    a2 = intListAppend(a2, 0)
    assert(a2 == 11111110)
    a2 = intListAppend(a2, 0)
    assert(a2 == 111211101110)
    print('Passed!')

def testIntSet():
    print('Testing intSet functions...', end='')
    s = newIntSet()
    assert(s == 1110) # [ 0 ]
    assert(intSetContains(s, 42) == False)
    s = intSetAdd(s, 42)
    assert(s == 111111242) # [ 1, 42]
    assert(intSetContains(s, 42) == True)
    s = intSetAdd(s, 42) # multiple adds --> still just one
    assert(s == 111111242) # [ 1, 42]
    assert(intSetContains(s, 42) == True)
    print('Passed!')

def testIntMap():
    print('Testing intMap functions...', end='')
    m = newIntMap()
    assert(m == 1110) # [ 0 ]
    assert(intMapContains(m, 42) == False)
    assert(intMapGet(m, 42) == 'no such key')
    m = intMapSet(m, 42, 73)
    assert(m == 11121124211273) # [ 2, 42, 73 ]
    assert(intMapContains(m, 42) == True)
    assert(intMapGet(m, 42) == 73)
    m = intMapSet(m, 42, 98765)
    assert(m == 11121124211598765) # [ 2, 42, 98765 ]
    assert(intMapGet(m, 42) == 98765)
    m = intMapSet(m, 99, 0)
    assert(m == 11141124211598765112991110) # [ 4, 42, 98765, 99, 0 ]
    assert(intMapGet(m, 42) == 98765)
    assert(intMapGet(m, 99) == 0)
    print('Passed!')

def testIntFSM():
    print('Testing intFSM functions...', end='')
    fsm = newIntFSM()
    assert(fsm == 111211411101141110) # [ empty stateMap, empty startStateSet ]
    assert(isAcceptingState(fsm, 1) == False)

    fsm = addAcceptingState(fsm, 1)
    assert(fsm == 1112114111011811111111)
    assert(isAcceptingState(fsm, 1) == True)

    assert(getTransition(fsm, 0, 8) == 'no such transition')
    fsm = setTransition(fsm, 4, 5, 6)
    # map[5] = 6: 111211151116
    # map[4] = (map[5] = 6):  111211141212111211151116
    assert(fsm == 1112122411121114121211121115111611811111111)
    assert(getTransition(fsm, 4, 5) == 6)

    fsm = setTransition(fsm, 4, 7, 8)
    fsm = setTransition(fsm, 5, 7, 9)
    assert(getTransition(fsm, 4, 5) == 6)
    assert(getTransition(fsm, 4, 7) == 8)
    assert(getTransition(fsm, 5, 7) == 9)

    fsm = newIntFSM()
    assert(fsm == 111211411101141110) # [ empty stateMap, empty startStateSet ]
    fsm = setTransition(fsm, 0, 5, 6)
    # map[5] = 6: 111211151116
    # map[0] = (map[5] = 6):  111211101212111211151116
    assert(fsm == 111212241112111012121112111511161141110)
    assert(getTransition(fsm, 0, 5) == 6)

    print('Passed!')

def testAccepts():
    print('Testing accepts()...', end='')
    fsm = newIntFSM()
    # fsm accepts 6*7+8
    fsm = addAcceptingState(fsm, 3)
    fsm = setTransition(fsm, 1, 6, 1) # 6* -> 1
    fsm = setTransition(fsm, 1, 7, 2) # 7 -> 2
    fsm = setTransition(fsm, 2, 7, 2) # 7* -> 2
    fsm = setTransition(fsm, 2, 8, 3) # 7* -> 3
    assert(accepts(fsm, 78) == True)
    assert(states(fsm, 78) == 1113111111121113) # [1,2,3]
    assert(accepts(fsm, 678) == True)
    assert(states(fsm, 678) == 11141111111111121113) # [1,1,2,3]

    assert(accepts(fsm, 5) == False)
    assert(accepts(fsm, 788) == False)
    assert(accepts(fsm, 67) == False)
    assert(accepts(fsm, 666678) == True)
    assert(accepts(fsm, 66667777777777778) == True)
    assert(accepts(fsm, 7777777777778) == True)
    assert(accepts(fsm, 666677777777777788) == False)
    assert(accepts(fsm, 77777777777788) == False)
    assert(accepts(fsm, 7777777777778) == True)
    assert(accepts(fsm, 67777777777778) == True)
    print('Passed!')

def testEncodeDecodeStrings():
    print('Testing encodeString and decodeString...', end='')
    assert(encodeString('A') == 111111265) # [1, 65]
    assert(encodeString('f') == 1111113102) # [1, 102]
    assert(encodeString('3') == 111111251) # [1, 51]
    assert(encodeString('!') == 111111233) # [1, 33]
    assert(encodeString('Af3!') == 1114112651131021125111233) # [4,65,102,51,33]
    assert(decodeString(111111265) == 'A')
    assert(decodeString(1114112651131021125111233) == 'Af3!')
    assert(decodeString(encodeString('WOW!!!')) == 'WOW!!!')
    print('Passed!')

def testIntegerDataStructures():
    testLengthEncode()
    testLengthDecode()
    testLengthDecodeLeftmostValue()
    testIntList()
    testIntSet()
    testIntMap()
    testIntFSM()
    testAccepts()
    testEncodeDecodeStrings()

#################################################
# testAll and main
#################################################

def testAll():
    # comment out the tests you do not wish to run!
    # required
    testDrawFancyWheels()

    # mild
    testMostFrequentDigit()
    testNthPalindromicPrime()
    testCarrylessAdd()
    testIntegral()
    testNthWithProperty309()
    testNthCircularPrime()

    # medium
    testFindZeroWithBisection()
    testNthSmithNumber()
    testCarrylessMultiply()
    testNthKaprekarNumber()
    testNthCarolPrime()

    # spicy
    testPlay112()
    testIntegerDataStructures()

def main():
    cs112_s20_unit2_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
