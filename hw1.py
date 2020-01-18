#################################################
# hw1.py
#
# Your name: Clara Ye
# Your andrew id: zixuany
#################################################

import cs112_s20_week1_linter
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

#################################################
# Functions for you to write
#################################################

def isEvenPositiveInt(x):
    if isinstance(x, int) == False:
        return False
    elif (x <= 0):
        return False
    elif (x % 2 == 1):
        return False
    else:
        return True

def nearestBusStop(street):
    distance = street % 8
    if (distance <= 4):
        return (street - distance)
    else:
        return (street - distance + 8)

def isPerfectSquare(n):
    if (isinstance(n, int) == False):
        return False
    elif (n < 0):
        return False
    else:
        return ((n ** 0.5) % 1 == 0)

def nthFibonacciNumber(n):
    if (n == 0) or (n == 1):
        return 1
    else:
        # calculate the constants
        Phi = (1 + 5 ** 0.5) / 2
        phi = (1 - 5 ** 0.5) / 2
        # use Binet's Fibonacci Number Formula
        nthFN = (Phi ** (n + 1) - phi ** (n + 1)) / (5 ** 0.5)
        return roundHalfUp(nthFN)

def numberOfPoolBalls(rows):
    return (((1 + rows) * rows) // 2)

def isFactorish(n):
    if (isinstance(n, int) == False):
        return False
    else:
        n = abs(n)
        # get each of the digits
        digit0 = n % 10
        digit1 = n // 10 % 10
        digit2 = n // 100
        # check that there are no more than 3 digits
        if digit2 >= 10:
            return False
        # check that none of the digits is 0
        elif digit0 == 0 or digit1 == 0 or digit2 == 0:
            return False
        # check that there are no duplicate digits
        elif digit0 == digit1 or digit1 == digit2 or digit0 == digit2:
            return False
        return True

def nearestOdd(n):
    roundedN = roundHalfUp(n)
    # return roundedN if it is odd
    if (roundedN % 2 == 1):
        return roundedN
    else:
        # if n rounds up, n would be closer to the smaller odd
        if (n <= roundedN):
            return (roundedN - 1)
        # if n rounds down, n would be closer to the larger odd
        else:
            return (roundedN + 1)

def rectanglesOverlap(x1, y1, w1, h1, x2, y2, w2, h2):
    # get the coordinates of the right and bottom of each rectangle
    r1 = x1 + w1
    r2 = x2 + w2
    b1 = y1 + h1
    b2 = y2 + h2
    # 4 conditions of not overlapping:
    # rectangle 1 is to the left, right, top, or bottom of rectangle 2
    if (r1 < x2) or (x1 > r2) or (b1 < y2) or (y1 > b2):
        return False
    else:
        return True

def numberOfPoolBallRows(balls):
    # use the quadratic formula
    rows = (-1 + (1 + 4 * 2 * balls) ** 0.5) / 2
    # ensure integer number of rows
    if (rows % 1 == 0):
        return int(rows)
    else:
        return (int(rows) + 1)

def lineIntersection(m1, b1, m2, b2):
    return ((b2 - b1) / (m1 - m2))

def distance(x1, y1, x2, y2):
    return (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)

def triangleArea(s1, s2, s3):
    # calculate the semi-perimeter
    s = (s1 + s2 + s3) / 2
    # use Heron's formula
    Area = (s * (s - s1) * (s - s2) * (s - s3)) ** 0.5
    return Area

def threeLinesArea(m1, b1, m2, b2, m3, b3):
    # find the coordinates
    x1 = lineIntersection(m1, b1, m2, b2)
    y1 = m1 * x1 + b1
    x2 = lineIntersection(m1, b1, m3, b3)
    y2 = m1 * x2 + b1
    x3 = lineIntersection(m2, b2, m3, b3)
    y3 = m2 * x3 + b2
    # find the lengths of the sides
    side1 = distance(x1, y1, x2, y2)
    side2 = distance(x1, y1, x3, y3)
    side3 = distance(x2, y2, x3, y3)
    return triangleArea(side1, side2, side3)

def colorBlender(rgb1, rgb2, midpoints, n):
    # return None if n is out of range (too small or too large)
    if (n < 0) or (n > (midpoints + 1)):
        return None
    else:
        # get the R, G, B values of the endpoints
        r1 = rgb1 // 1000000
        r2 = rgb2 // 1000000
        g1 = (rgb1 % 1000000) // 1000
        g2 = (rgb2 % 1000000) // 1000
        b1 = rgb1 % 1000
        b2 = rgb2 % 1000
        # calculate the abosolute difference between endpoints
        diffR = abs(r1 - r2) / (midpoints + 1)
        diffG = abs(g1 - g2) / (midpoints + 1)
        diffB = abs(b1 - b2) / (midpoints + 1)
        # calculate the R, G, B values of the nth color in the palette
        if r1 < r2:
            r = r1 + n * diffR
        else:
            r = r1 - n * diffR
        if g1 < g2:
            g = g1 + n * diffG
        else:
            g = g1 - n * diffG
        if b1 < b2:
            b = b1 + n * diffB
        else:
            b = b1 - n * diffB
        # round the values to integers
        r = roundHalfUp(r)
        g = roundHalfUp(g)
        b = roundHalfUp(b)
        # return the RGB value as a single integer
        return ((r * 1000000) + (g * 1000) + b)
        
def handToDice(hand):
    a = hand // 100
    b = (hand % 100) // 10
    c = hand % 10
    return (a, b, c)

def orderDice(a, b, c):
    # get the large and small value
    large = max(a, b, c)
    small = min(a, b, c)
    # get the medium value
    medium = (a + b + c) - (large + small)
    # return ordered Dice
    return (large, medium, small)

def diceToOrderedHand(a, b, c):
    # order the dice
    (large, medium, small) = orderDice(a, b, c)
    # return the hand
    return ((large * 100) + (medium * 10) + small)

def playStep2(hand, dice):
    (a, b, c) = handToDice(hand)
    (large, medium, small) = orderDice(a, b, c)
    if (large == small):
        return (hand, dice)
    elif (large == medium):
        new = dice % 10
        dice //= 10
        hand = diceToOrderedHand(large, medium, new)
        return (hand, dice)
    elif (medium == small):
        new = dice % 10
        dice //= 10
        hand = diceToOrderedHand(new, medium, small)
        return (hand, dice)
    else:
        new1 = dice % 10
        dice //= 10
        new2 = dice % 10
        dice //= 10
        hand = diceToOrderedHand(large, new1, new2)
        return (hand, dice)

def score(hand):
    (large, medium, small) = handToDice(hand)
    if (large == small):
        return (20 + large + medium + small)
    elif (large == medium):
        return (10 + large + medium)
    elif (medium == small):
        return (10 + medium + small)
    else:
        return large

def playThreeDiceYahtzee(dice):
    hand = dice % 1000
    dice //= 1000
    (hand, dice) = playStep2(hand,dice)
    (hand, dice) = playStep2(hand,dice)
    return (hand, score(hand))

def real(z):
    return (complex(z)).real # since in 2.5 non-complex don't have .real

def findIntRootsOfCubic(a, b, c, d):
    # calculate the constants
    p = -b / (3 * a)
    q = (p ** 3) + (((b * c) - (3 * a * d)) / (6 * a ** 2))
    r = c / (3 * a)
    m = ((q ** 2) + (r - p ** 2) ** 3) ** 0.5
    # use Cardano's cubic formula to find one root
    x1 = ((q + m) ** (1 / 3)) + ((q - m) ** (1 / 3)) + p
    # convert x1 to real integer
    x1 = roundHalfUp(real(x1))
    # devide one root out
    b = b + a * x1
    c = -d / x1
    # solve the quadratic equation to get the other roots
    n = ((b ** 2) - (4 * a * c)) ** 0.5
    x2 = (-b + n) / (2 * a)
    x2 = roundHalfUp(real(x2))
    x3 = (-b - n) / (2 * a)
    x3 = roundHalfUp(real(x3))
    # sort the roots so root1 is min and root3 is max
    root1 = min(x1, x2, x3)
    root3 = max(x1, x2, x3)
    root2 = (x1 + x2 + x3) - (root1 + root3)
    return (root1, root2, root3)

#################################################
# Test Functions
#################################################

def testIsEvenPositiveInt():
    print('Testing isEvenPositiveInt()... ', end='')
    assert(isEvenPositiveInt(809) == False)
    assert(isEvenPositiveInt(810) == True)
    assert(isEvenPositiveInt(2389238001) == False)
    assert(isEvenPositiveInt(2389238000) == True)
    assert(isEvenPositiveInt(-2389238000) == False)
    assert(isEvenPositiveInt(0) == False)
    assert(isEvenPositiveInt('do not crash here!') == False)
    print('Passed.')

def testNearestBusStop():
    print('Testing nearestBusStop()... ', end='')
    assert(nearestBusStop(0) == 0)
    assert(nearestBusStop(4) == 0)
    assert(nearestBusStop(5) == 8)
    assert(nearestBusStop(12) == 8)
    assert(nearestBusStop(13) == 16)
    assert(nearestBusStop(20) == 16)
    assert(nearestBusStop(21) == 24)
    print('Passed.')

def testIsPerfectSquare():
    print('Testing isPerfectSquare()... ', end='')
    assert(isPerfectSquare(0) == True)
    assert(isPerfectSquare(1) == True)
    assert(isPerfectSquare(16) == True)
    assert(isPerfectSquare(1234**2) == True)
    assert(isPerfectSquare(15) == False)
    assert(isPerfectSquare(17) == False)
    assert(isPerfectSquare(-16) == False)
    assert(isPerfectSquare(1234**2+1) == False)
    assert(isPerfectSquare(1234**2-1) == False)
    assert(isPerfectSquare(4.0000001) == False)
    assert(isPerfectSquare('Do not crash here!') == False)
    print('Passed.')

def testNthFibonacciNumber():
    print('Testing nthFibonacciNumber()... ', end='')
    assert(nthFibonacciNumber(0) == 1)
    assert(nthFibonacciNumber(1) == 1)
    assert(nthFibonacciNumber(2) == 2)
    assert(nthFibonacciNumber(3) == 3)
    assert(nthFibonacciNumber(4) == 5)
    assert(nthFibonacciNumber(5) == 8)
    assert(nthFibonacciNumber(6) == 13)
    print('Passed.')

def testNumberOfPoolBalls():
    print('Testing numberOfPoolBalls()... ', end='')
    assert(numberOfPoolBalls(0) == 0)
    assert(numberOfPoolBalls(1) == 1)
    assert(numberOfPoolBalls(2) == 3)   # 1+2 == 3
    assert(numberOfPoolBalls(3) == 6)   # 1+2+3 == 6
    assert(numberOfPoolBalls(10) == 55) # 1+2+...+10 == 55
    print('Passed.')

def testIsFactorish():
    print('Testing isFactorish()...', end='')
    assert(isFactorish(412) == True)      # 4, 1, and 2 are all factors of 412
    assert(isFactorish(-412) == True)     # Must work for negative numbers!
    assert(isFactorish(4128) == False)    # has more than 3 digits
    assert(isFactorish(112) == False)     # has duplicates digits (two 1's)
    assert(isFactorish(420) == False)     # has a 0 (no 0's allowed)
    assert(isFactorish(42) == False)      # has a leading 0 (no 0's allowed)
    assert(isFactorish(1.0) == False)     # floats are not factorish
    assert(isFactorish('nope!') == False) # don't crash on strings
    print('Passed!')

def testNearestOdd():
    print('Testing nearestOdd()... ', end='')
    assert(nearestOdd(13) == 13)
    assert(nearestOdd(12.001) == 13)
    assert(nearestOdd(12) == 11)
    assert(nearestOdd(11.999) == 11)
    assert(nearestOdd(-13) == -13)
    assert(nearestOdd(-12.001) == -13)
    assert(nearestOdd(-12) == -13)
    assert(nearestOdd(-11.999) == -11)
    # results must be int's not floats
    assert(isinstance(nearestOdd(13.0), int))
    assert(isinstance(nearestOdd(11.999), int))
    print('Passed.')

def testRectanglesOverlap():
    print('Testing rectanglesOverlap()...', end='')
    assert(rectanglesOverlap(1, 1, 2, 2, 2, 2, 2, 2) == True)
    assert(rectanglesOverlap(1, 1, 2, 2, -2, -2, 6, 6) == True)
    assert(rectanglesOverlap(1, 1, 2, 2, 3, 3, 1, 1) == True)
    assert(rectanglesOverlap(1, 1, 2, 2, 3.1, 3, 1, 1) == False)
    assert(rectanglesOverlap(1, 1, 1, 1, 1.9, -1, 0.2, 1.9) == False)
    assert(rectanglesOverlap(1, 1, 1, 1, 1.9, -1, 0.2, 2) == True)
    assert(rectanglesOverlap(1, 1, 2, 2, 2, 2, 2, 6) == True)
    assert(rectanglesOverlap(1, 1, 2, 2, 3,4,5,6) == False)
    print('Passed.')

def testNumberOfPoolBallRows():
    print('Testing numberOfPoolBallRows()... ', end='')
    assert(numberOfPoolBallRows(0) == 0)
    assert(numberOfPoolBallRows(1) == 1)
    assert(numberOfPoolBallRows(2) == 2)
    assert(numberOfPoolBallRows(3) == 2)
    assert(numberOfPoolBallRows(4) == 3)
    assert(numberOfPoolBallRows(6) == 3)
    assert(numberOfPoolBallRows(7) == 4)
    assert(numberOfPoolBallRows(10) == 4)
    assert(numberOfPoolBallRows(11) == 5)
    assert(numberOfPoolBallRows(55) == 10)
    assert(numberOfPoolBallRows(56) == 11)
    print('Passed.')

def testThreeLinesArea():
    print('Testing threeLinesArea()... ', end='')
    assert(almostEqual(threeLinesArea(1, 2, 3, 4, 5, 6), 0))
    assert(almostEqual(threeLinesArea(0, 7, 1, 0, -1, 2), 36))
    assert(almostEqual(threeLinesArea(0, 3, -.5, -5, 1, 3), 42.66666666666666))
    assert(almostEqual(threeLinesArea(1, -5, 0, -2, 2, 2), 25))
    assert(almostEqual(threeLinesArea(0, -9.75, -6, 2.25, 1, -4.75), 21))
    assert(almostEqual(threeLinesArea(1, -5, 0, -2, 2, 25), 272.25))
    print('Passed.')

def testColorBlender():
    print('Testing colorBlender()... ', end='')
    # http://meyerweb.com/eric/tools/color-blend/#DC143C:BDFCC9:3:rgbd
    assert(colorBlender(220020060, 189252201, 3, -1) == None)
    assert(colorBlender(220020060, 189252201, 3, 0) == 220020060)
    assert(colorBlender(220020060, 189252201, 3, 1) == 212078095)
    assert(colorBlender(220020060, 189252201, 3, 2) == 205136131)
    assert(colorBlender(220020060, 189252201, 3, 3) == 197194166)
    assert(colorBlender(220020060, 189252201, 3, 4) == 189252201)
    assert(colorBlender(220020060, 189252201, 3, 5) == None)
    # http://meyerweb.com/eric/tools/color-blend/#0100FF:FF0280:2:rgbd
    assert(colorBlender(1000255, 255002128, 2, -1) == None)
    assert(colorBlender(1000255, 255002128, 2, 0) == 1000255)
    assert(colorBlender(1000255, 255002128, 2, 1) == 86001213)
    assert(colorBlender(1000255, 255002128, 2, 2) == 170001170)
    assert(colorBlender(1000255, 255002128, 2, 3) == 255002128)
    print('Passed.')

def testPlayThreeDiceYahtzee():
    print('Testing playThreeDiceYahtzee()...', end='')
    assert(handToDice(123) == (1,2,3))
    assert(handToDice(214) == (2,1,4))
    assert(handToDice(422) == (4,2,2))
    assert(diceToOrderedHand(1,2,3) == 321)
    assert(diceToOrderedHand(6,5,4) == 654)
    assert(diceToOrderedHand(1,4,2) == 421)
    assert(diceToOrderedHand(6,5,6) == 665)
    assert(diceToOrderedHand(2,2,2) == 222)
    assert(playStep2(413, 2312) == (421, 23))
    assert(playStep2(421, 23) == (432, 0))
    assert(playStep2(413, 2345) == (544, 23))
    assert(playStep2(544, 23) == (443, 2))
    assert(playStep2(544, 456) == (644, 45))
    assert(score(432) == 4)
    assert(score(532) == 5)
    assert(score(443) == 10+4+4)
    assert(score(633) == 10+3+3)
    assert(score(333) == 20+3+3+3)
    assert(score(555) == 20+5+5+5)
    assert(playThreeDiceYahtzee(2312413) == (432, 4))
    assert(playThreeDiceYahtzee(2315413) == (532, 5))
    assert(playThreeDiceYahtzee(2345413) == (443, 18))
    assert(playThreeDiceYahtzee(2633413) == (633, 16))
    assert(playThreeDiceYahtzee(2333413) == (333, 29))
    assert(playThreeDiceYahtzee(2333555) == (555, 35))
    print('Passed!')

def getCubicCoeffs(k, root1, root2, root3):
    # Given roots e,f,g and vertical scale k, we can find
    # the coefficients a,b,c,d as such:
    # k(x-e)(x-f)(x-g) =
    # k(x-e)(x^2 - (f+g)x + fg)
    # kx^3 - k(e+f+g)x^2 + k(ef+fg+eg)x - kefg
    e,f,g = root1, root2, root3
    return k, -k*(e+f+g), k*(e*f+f*g+e*g), -k*e*f*g

def testFindIntRootsOfCubicCase(k, z1, z2, z3):
    a,b,c,d = getCubicCoeffs(k, z1, z2, z3)
    result1, result2, result3 = findIntRootsOfCubic(a,b,c,d)
    m1 = min(z1, z2, z3)
    m3 = max(z1, z2, z3)
    m2 = (z1+z2+z3)-(m1+m3)
    actual = (m1, m2, m3)
    assert(almostEqual(m1, result1))
    assert(almostEqual(m2, result2))
    assert(almostEqual(m3, result3))

def testFindIntRootsOfCubic():
    print('Testing findIntRootsOfCubic()...', end='')
    testFindIntRootsOfCubicCase(5, 1, 3,  2)
    testFindIntRootsOfCubicCase(2, 5, 33, 7)
    testFindIntRootsOfCubicCase(-18, 24, 3, -8)
    testFindIntRootsOfCubicCase(1, 2, 3, 4)
    print('Passed.')

#################################################
# testAll and main
#################################################

def testAll():
    # comment out the tests you do not wish to run!
    # mild
    testIsEvenPositiveInt()
    testNearestBusStop()
    testIsPerfectSquare()
    testNthFibonacciNumber()
    testNumberOfPoolBalls()
    testIsFactorish()
    testNearestOdd()

    # medium
    testRectanglesOverlap()
    testNumberOfPoolBallRows()
    testThreeLinesArea()

    # spicy
    testColorBlender()
    testPlayThreeDiceYahtzee()
    testFindIntRootsOfCubic()

def main():
    cs112_s20_week1_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
