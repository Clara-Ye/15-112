#################################################
# writing_session2_practice.py
#
# Your name: Clara Ye
# Your andrew id: zixuany
#################################################

import cs112_s20_unit2_linter
import basic_graphics

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

def digitCount(n):
    n = abs(n)
    count = 1
    while (n > 10):
        n //= 10
        count += 1
    return count

def gcd(m, n):
    while (n > 0):
        temp = n
        n = m % n
        m = temp
    return m

def hasConsecutiveDigits(n):
    n = abs(n)
    while (n > 0):
        ones = n % 10
        tens = (n % 100) // 10
        if (ones == tens):
            return True
        else:
            n //= 10
    return False

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

def nthPrime(n):
    count = 0
    guess = 2
    while (count < n):
        guess += 1
        if isPrime(guess):
            count += 1
    return guess

def sumDigits(n):
    total = 0
    while (n > 0):
        digit = n % 10
        total += digit
        n //= 10
    return total

def nthAdditivePrime(n):
    count = 0
    guess = 2
    while (count < n):
        guess += 1
        if isPrime(guess) and isPrime(sumDigits(guess)):
            count += 1
    return guess

def drawDashedLine(canvas, width, height, dashLength):
    midHeight = height // 2
    left = 0
    while (left < width):
        canvas.create_line(left, midHeight, 
                          (left + dashLength), midHeight)
        left += 2 * dashLength
    return None

#################################################
# Test Functions
#################################################

def testDigitCount():
    print('Testing digitCount()...', end='')
    assert(digitCount(3) == 1)
    assert(digitCount(33) == 2)
    assert(digitCount(3030) == 4)
    assert(digitCount(-3030) == 4)
    assert(digitCount(0) == 1)
    print('Passed.')

def testGcd():
    print('Testing gcd()...', end='')
    assert(gcd(3, 3) == 3)
    assert(gcd(3**6, 3**6) == 3**6)
    assert(gcd(3**6, 2**6) == 1)
    assert (gcd(2*3*4*5,3*5) == 15)
    x = 1568160 # 2**5 * 3**4 * 5**1 *        11**2
    y = 3143448 # 2**3 * 3**6 *        7**2 * 11**1
    g =    7128 # 2**3 * 3**4 *               11**1
    assert(gcd(x, y) == g)
    print('Passed.')

def testHasConsecutiveDigits():
    print('Testing hasConsecutiveDigits()...', end='')
    assert(hasConsecutiveDigits(0) == False)
    assert(hasConsecutiveDigits(123456789) == False)
    assert(hasConsecutiveDigits(1212) == False)
    assert(hasConsecutiveDigits(1212111212) == True)
    assert(hasConsecutiveDigits(33) == True)
    assert(hasConsecutiveDigits(-1212111212) == True)
    print('Passed.')

def testNthPrime():
    print('Testing nthPrime()... ', end='')
    assert(nthPrime(0) == 2)
    assert(nthPrime(1) == 3)
    assert(nthPrime(2) == 5)
    assert(nthPrime(3) == 7)
    assert(nthPrime(10) == 31)
    assert(nthPrime(20) == 73)
    assert(nthPrime(30) == 127)
    print('Passed.')

def testNthAdditivePrime():
    print('Testing nthAdditivePrime()... ', end='')
    assert(nthAdditivePrime(0) == 2)
    assert(nthAdditivePrime(1) == 3)
    assert(nthAdditivePrime(5) == 23)
    assert(nthAdditivePrime(10) == 61)
    assert(nthAdditivePrime(15) == 113)
    print('Passed.')

def testDrawDashedLine():
    print('Testing drawDashedLine()... (confirm visually)')
    print('  drawDashedLine: dashLength of 5, win size of 400x400...', end='')
    basic_graphics.run(5, width=400, height=400, drawFn=drawDashedLine)
    print('  drawDashedLine: dashLength of 20, win size of 800x200...', end='')
    basic_graphics.run(20, width=800, height=200, drawFn=drawDashedLine)

#################################################
# testAll and main
#################################################

def testAll():
    testDigitCount()
    testGcd()   
    testHasConsecutiveDigits()   
    testNthPrime()
    testNthAdditivePrime()
    testDrawDashedLine()

def main():
    cs112_s20_unit2_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
