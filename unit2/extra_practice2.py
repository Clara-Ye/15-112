#################################################
# extra_practice2.py
#
# Your name:
# Your andrew id:
#################################################

import cs112_s20_unit2_linter
import math
from tkinter import *

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
################################################

def longestDigitRun(n):
    n = abs(n)
    # if n has only 1 digit, it is the longest digit:
    if (n < 10):
        return n
    else:
        currentRun = 1
        currentDigit = 99
        longestRun = currentRun
        longestDigit = currentDigit
        while (n > 10):
            currentDigit = n % 10
            nextDigit = (n % 100) // 10
            n //= 10
            if (currentDigit == nextDigit):
                currentRun += 1
                # compare current run with longest run,
                # update values when needed:
                if (currentRun > longestRun):
                    longestRun = currentRun
                    longestDigit = currentDigit
                elif ((currentRun == longestRun) and 
                    (currentDigit < longestDigit)):
                    longestDigit = currentDigit
            # next digit is different, reset:
            else:
                currentRun = 1
        return longestDigit

def isPrime(n):
    if (n < 2):
        return False
    elif (n == 2):
        return True
    elif (n % 2 == 0):
        return False
    else:
        for guess in range(3, roundHalfUp(n**0.5)+1, 2):
            if (n % guess == 0):
                return False
        return True      

def digitCount(n):
    n = abs(n)
    count = 1
    while (n > 10):
        n //= 10
        count += 1
    return count

def isLeftTruncatablePrime(n):
    if (isPrime(n) == False):
        return False
    else:
        digit = digitCount(n)
        for i in range(1, digit):
            guess = n % (10**i)
            if (isPrime(guess) == False):
                return False
        return True
        
def nthLeftTruncatablePrime(n):
    guess = 2
    count = 0
    while (count < n):
        guess += 1
        if isLeftTruncatablePrime(guess):
            count += 1
    return guess

def sumOfSquaresOfDigits(n):
    total = 0
    while (n > 0):
        digit = n % 10
        total += digit ** 2
        n = n // 10
    return total

def isHappyNumber(n):
    if (n <= 0) or (n == 4):
        return False
    elif (n == 1):
        return True
    else:
        while True:
            n = sumOfSquaresOfDigits(n)
            if (n == 1):
                return True
            if (n == 4):
                return False

def nthHappyNumber(n):
    guess = 1
    count = 0
    while (count < n):
        guess += 1
        if isHappyNumber(guess):
            count += 1
    return guess

def isHappyPrime(n):
    return isHappyNumber(n) and isPrime(n)

def nthHappyPrime(n):
    guess = 7
    count = 0
    while (count < n):
        guess += 1
        if isHappyPrime(guess):
            count += 1
    return guess

def isPowerfulNumber(n):
    factor = 2
    while (n > 1):
        if (n % factor == 0):
            if (n % (factor**2) != 0):
                return False
            while (n > 1) and (n % factor == 0):
                n //= factor
        else:
            factor += 1
    return True

def nthPowerfulNumber(n):
    guess = 1
    count = 0
    while (count < n):
        guess += 1
        if isPowerfulNumber(guess):
            count += 1
    return guess

#################################################
# Test Functions
#################################################

def testLongestDigitRun():
    print('Testing longestDigitRun()... ', end='')
    assert(longestDigitRun(117773732) == 7)
    assert(longestDigitRun(-677886) == 7)
    assert(longestDigitRun(5544) == 4)
    assert(longestDigitRun(1) == 1)
    assert(longestDigitRun(0) == 0)
    assert(longestDigitRun(22222) == 2)
    assert(longestDigitRun(111222111) == 1)
    print('Passed.')

def testNthLeftTruncatablePrime():
    print('Testing nthLeftTruncatablePrime()... ', end='')
    assert(nthLeftTruncatablePrime(0) == 2)
    assert(nthLeftTruncatablePrime(10) == 53)
    assert(nthLeftTruncatablePrime(1) == 3)
    assert(nthLeftTruncatablePrime(5) == 17)
    print('Passed.')

def testSumOfSquaresOfDigits():
    print("Testing sumOfSquaresOfDigits()...", end="")
    assert(sumOfSquaresOfDigits(5) == 25)   # 5**2 = 25
    assert(sumOfSquaresOfDigits(12) == 5)   # 1**2 + 2**2 = 1+4 = 5
    assert(sumOfSquaresOfDigits(234) == 29) # 2**2 + 3**2 + 4**2 = 4+9+16 = 29
    print("Passed.")

def testIsHappyNumber():
    print("Testing isHappyNumber()...", end="")
    assert(isHappyNumber(-7) == False)
    assert(isHappyNumber(1) == True)
    assert(isHappyNumber(2) == False)
    assert(isHappyNumber(97) == True)
    assert(isHappyNumber(98) == False)
    assert(isHappyNumber(404) == True)
    assert(isHappyNumber(405) == False)
    print("Passed.")

def testNthHappyNumber():
    print("Testing nthHappyNumber()...", end="")
    assert(nthHappyNumber(0) == 1)
    assert(nthHappyNumber(1) == 7)
    assert(nthHappyNumber(2) == 10)
    assert(nthHappyNumber(3) == 13)
    assert(nthHappyNumber(4) == 19)
    assert(nthHappyNumber(5) == 23)
    assert(nthHappyNumber(6) == 28)
    assert(nthHappyNumber(7) == 31)
    print("Passed.")

def testIsHappyPrime():
    print("Testing isHappyPrime()...", end="")
    assert(isHappyPrime(1) == False)
    assert(isHappyPrime(2) == False)
    assert(isHappyPrime(3) == False)
    assert(isHappyPrime(7) == True)
    assert(isHappyPrime(10) == False)
    assert(isHappyNumber(13) == True)
    print("Passed.")

def testNthHappyPrime():
    print("Testing nthHappyPrime...", end="")
    assert(nthHappyPrime(0) == 7)
    assert(nthHappyPrime(1) == 13)
    assert(nthHappyPrime(2) == 19)
    assert(nthHappyPrime(3) == 23)
    assert(nthHappyPrime(4) == 31)
    assert(nthHappyPrime(10) == 167)
    assert(nthHappyPrime(20) == 397)
    print("Passed.")

def testNthPowerfulNumber():
    print('Testing nthPowerfulNumber()... ', end='')
    assert(nthPowerfulNumber(0) == 1)
    assert(nthPowerfulNumber(1) == 4)
    assert(nthPowerfulNumber(2) == 8)
    assert(nthPowerfulNumber(3) == 9)
    assert(nthPowerfulNumber(4) == 16)
    assert(nthPowerfulNumber(5) == 25)
    assert(nthPowerfulNumber(10) == 64)
    assert(nthPowerfulNumber(15) == 121)
    assert(nthPowerfulNumber(20) == 196)
    print('Passed.')

#################################################
# testAll and main
#################################################

def testAll():
    testLongestDigitRun()
    testNthLeftTruncatablePrime()
    testSumOfSquaresOfDigits()
    testIsHappyNumber()
    testNthHappyNumber()
    testIsHappyPrime()
    testNthHappyPrime()
    testNthPowerfulNumber()

def main():
    cs112_s20_unit2_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
