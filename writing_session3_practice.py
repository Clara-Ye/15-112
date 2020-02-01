#################################################
# writing_session3_practice.py
#################################################

import cs112_s20_unit3_linter
import string

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

def vowelCount(s):
    vowels = "AEIOUaeiou"
    count = 0
    for c in s:
        if c in vowels:
            count += 1
    return count

def rotateStringLeft(s, n):
    # if n is negative, will be negative indexing
    i = n % len(s)
    return (s[i:] + s[:i])

def rotateStringRight(s, n):
    return rotateStringLeft(s, -n)

def isRotation(s, t):
    for n in range(1, len(s)):
        if (t == rotateStringLeft(s, n)):
            return True
    return False

def shiftCharacter(c, shift, baseChar):
    offset = ord(c) - ord(baseChar)
    newOffset = (offset + shift) % 26
    newChar = chr(ord(baseChar) + newOffset)
    return newChar

def applyCaesarCipher(message, shift):
    cipher = ""
    for c in message:
        if (not c.isalpha()):
            cipher += c
        elif (c.isupper()):
            cipher += shiftCharacter(c, shift, "A")
        else:
            cipher += shiftCharacter(c, shift, "a")
    return cipher

def collapseWhitespace(s):
    # first c will be in the new string no matter it's whitespace or not:
    newS = s[0]
    for i in range(1, len(s)):
        if (not s[i].isspace()):
            newS += s[i]
        # if current c is whitespace and previous c is not, add a whitespace:
        elif (not s[i-1].isspace()):
            newS += " "
    return newS

#################################################
# Test Functions
#################################################

def testVowelCount():
    print('Testing vowelCount()...', end='')
    assert(vowelCount('abcdefg') == 2)
    assert(vowelCount('ABCDEFG') == 2)
    assert(vowelCount('') == 0)
    assert(vowelCount('This is a test.  12345.') == 4)
    assert(vowelCount(string.ascii_lowercase) == 5)
    assert(vowelCount(string.ascii_lowercase*100) == 500)
    assert(vowelCount(string.ascii_uppercase) == 5)
    assert(vowelCount(string.punctuation) == 0)
    assert(vowelCount(string.whitespace) == 0)
    print('Passed!')

def testRotateStringLeft():
    print('Testing rotateStringLeft()...', end='')
    assert(rotateStringLeft('abcde', 0) == 'abcde')
    assert(rotateStringLeft('abcde', 1) == 'bcdea')
    assert(rotateStringLeft('abcde', 2) == 'cdeab')
    assert(rotateStringLeft('abcde', 3) == 'deabc')
    assert(rotateStringLeft('abcde', 4) == 'eabcd')
    assert(rotateStringLeft('abcde', 5) == 'abcde')
    assert(rotateStringLeft('abcde', 25) == 'abcde')
    assert(rotateStringLeft('abcde', 28) == 'deabc')
    assert(rotateStringLeft('abcde', -1) == 'eabcd')
    assert(rotateStringLeft('abcde', -24) == 'bcdea')
    assert(rotateStringLeft('abcde', -25) == 'abcde')
    assert(rotateStringLeft('abcde', -26) == 'eabcd')
    print('Passed!')
    
def testRotateStringRight():
    print('Testing rotateStringRight()...', end='')
    assert(rotateStringRight('abcde', 0) == 'abcde')
    assert(rotateStringRight('abcde', 1) == 'eabcd')
    assert(rotateStringRight('abcde', 2) == 'deabc')
    assert(rotateStringRight('abcde', 3) == 'cdeab')
    assert(rotateStringRight('abcde', 4) == 'bcdea')
    assert(rotateStringRight('abcde', 5) == 'abcde')
    assert(rotateStringRight('abcde', 25) == 'abcde')
    assert(rotateStringRight('abcde', 28) == 'cdeab')
    assert(rotateStringRight('abcde', -1) == 'bcdea')
    assert(rotateStringRight('abcde', -24) == 'eabcd')
    assert(rotateStringRight('abcde', -25) == 'abcde')
    assert(rotateStringRight('abcde', -26) == 'bcdea')
    print('Passed!')

def testIsRotation():
    print('Testing isRotation()...', end='')
    assert(isRotation('a', 'a') == False) # a string is not a rotation of itself
    assert(isRotation('', '') == False) # a string is not a rotation of itself
    assert(isRotation('ab', 'ba') == True)
    assert(isRotation('abcd', 'dabc') == True)
    assert(isRotation('abcd', 'cdab') == True)
    assert(isRotation('abcd', 'bcda') == True)
    assert(isRotation('abcd', 'abcd') == False)
    assert(isRotation('abcd', 'bcd') == False)
    assert(isRotation('abcd', 'bcdx') == False)
    print('Passed!')

def testApplyCaesarCipher():
    print('Testing applyCaesarCipher()...', end='')
    assert(applyCaesarCipher('abcdefghijklmnopqrstuvwxyz', 3) ==
                             'defghijklmnopqrstuvwxyzabc')
    assert(applyCaesarCipher('We Attack At Dawn', 1) == 'Xf Buubdl Bu Ebxo')
    assert(applyCaesarCipher('1234', 6) == '1234')
    assert(applyCaesarCipher('abcdefghijklmnopqrstuvwxyz', 25) ==
                             'zabcdefghijklmnopqrstuvwxy')
    assert(applyCaesarCipher('We Attack At Dawn', 2)  == 'Yg Cvvcem Cv Fcyp')
    assert(applyCaesarCipher('We Attack At Dawn', 4)  == 'Ai Exxego Ex Hear')
    assert(applyCaesarCipher('We Attack At Dawn', -1) == 'Vd Zsszbj Zs Czvm')
    # And now, the whole point...
    assert(applyCaesarCipher(applyCaesarCipher('This is Great', 25), -25)
           == 'This is Great')
    print('Passed.')

def testCollapseWhitespace():
    print('Testing collapseWhitespace()...', end='')
    assert(collapseWhitespace('a\nb') == 'a b')
    assert(collapseWhitespace('a\n   \t    b') == 'a b')
    assert(collapseWhitespace('a\n   \t    b  \n\n  \t\t\t c   ') == 'a b c ')
    assert(collapseWhitespace('abc') == 'abc')
    assert(collapseWhitespace('   \n\n  \t\t\t  ') == ' ')
    assert(collapseWhitespace(' A  \n\n  \t\t\t z  \t\t ') == ' A z ')
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testVowelCount()
    testRotateStringLeft()
    testRotateStringRight()
    testIsRotation()
    testApplyCaesarCipher()
    testCollapseWhitespace()

def main():
    cs112_s20_unit3_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
