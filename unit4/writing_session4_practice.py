#################################################
# writing_session4_practice_solutions.py
#################################################

import cs112_s20_unit4_linter
import math, copy

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

# returns the alternating sum of a list of numbers
# (where the sign alternates from positive to negative or vice versa):
def alternatingSum(L):
    total = 0
    for i in range(len(L)):
        if (i % 2 == 0):
            total += L[i]
        else:
            total -= L[i]
    return total

# returns the median value of a list of numbers:
def median(L):
    if (L == []):
        return None
    else:
        L = sorted(L)
        n = len(L)
        if (n % 2 == 0):
            return ((L[n//2] + L[(n//2)-1]) / 2)
        else:
            return L[n//2]

# checks if a list is sorted, either in ascending or descending order:
def isSorted(L):
    if (len(L) <= 2):
        return True
    elif (L[0] < L[-1]):
        for i in range(len(L)-1):
            if (L[i] > L[i+1]):
                return False
    else:
        for i in range(len(L)-1):
            if (L[i] < L[i+1]):
                return False
    return True

# finds the smallest absolute difference between any two integers in a list:
def smallestDifference(L):
    if (len(L) <= 2):
        return -1
    else:
        minDiff = None
        for i in range(len(L)-1):
            for j in range(i+1, len(L)):
                currDiff = abs(L[i] - L[j])
                if (minDiff == None) or (currDiff < minDiff):
                    minDiff = currDiff
        return minDiff

# takes a list of numbers and returns a list of numbers that results from 
# "reading off" the initial list using the look-and-say method:
def lookAndSay(L):
    result = []
    count = 1
    for i in range(len(L)):
        if ((i+1) < len(L)) and (L[i] == L[i+1]):
            count += 1
        else: 
            result.append((count, L[i]))
            count = 1
    return result

# generates the corresponding numbers given a list look-and-say numbers:
def inverseLookAndSay(L):
    result = []
    for (count, num) in L:
        result += [num]*count
    return result

# removes repeating elements in a list nondestructively:
def nondestructiveRemoveRepeats(L):
    N = []
    for item in L:
        if (item not in N):
            N.append(item)
    return N

# removes repeating elements in a list destructively:
def destructiveRemoveRepeats(L):
    i = 0
    while (i < len(L)):
        if L[i] in L[:i]:
            L.pop(i)
        else:
            i += 1

class VoteTally(object):
    
    # a VoteTally object has properties candidates (a list of candidate names)
    # and counts (a list of votes for corresponding candidates):
    def __init__(self, candidates):
        self.candidates = candidates
        self.counts = [0] * len(candidates)

    # adds votes to a given candidate:
    def addVotes(self, votes, candidate):
        if (candidate not in self.candidates):
            return f"No such candidate as {candidate}"
        else:
            i = self.candidates.index(candidate)
            self.counts[i] += votes

    # gets total votes or the votes of a given candidate:
    def getVotes(self, candidate):
        if (candidate == "Total"):
            return sum(self.counts)
        elif (candidate not in self.candidates):
            return f"No such candidate as {candidate}"
        else:
            i = self.candidates.index(candidate)
            return self.counts[i]

    # combines two vote tallies into a new vote tally:
    def addVoteTally(self, other):
        newCandidates = copy.copy(self.candidates)
        newCounts = copy.copy(self.counts)
        for i in range(len(other.candidates)):
            if (other.candidates[i] in newCandidates):
                # add the votes of candidates that appear in both tallies:
                newCounts[i] += other.counts[i]
            else:
                newCandidates.append(other.candidates[i])
                newCounts.append(other.counts[i])
        # create the new vote tally:
        newVT = VoteTally(newCandidates)
        newVT.counts = newCounts
        return newVT

#################################################
# Test Functions
#################################################

def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(alternatingSum([ ]) == 0)
    assert(alternatingSum([1]) == 1)
    assert(alternatingSum([1, 5]) == 1-5)
    assert(alternatingSum([1, 5, 17]) == 1-5+17)
    assert(alternatingSum([1, 5, 17, 4]) == 1-5+17-4)
    print('Passed.')

def testMedian():
    print('Testing median()...', end='')
    assert(median([ ]) == None)
    assert(median([ 42 ]) == 42)
    assert(almostEqual(median([ 1 ]), 1))
    assert(almostEqual(median([ 1, 2]), 1.5))
    assert(almostEqual(median([ 2, 3, 2, 4, 2]), 2))
    assert(almostEqual(median([ 2, 3, 2, 4, 2, 3]), 2.5))
    # now make sure this is non-destructive
    a = [ 2, 3, 2, 4, 2, 3]
    b = a + [ ]
    assert(almostEqual(median(b), 2.5))
    if (a != b):
        raise Exception('Your median() function should be non-destructive!')
    print('Passed')

def testIsSorted():
    print('Testing isSorted()...', end='')
    assert(isSorted([]) == True)
    assert(isSorted([1]) == True)
    assert(isSorted([1,1]) == True)
    assert(isSorted([1,2]) == True)
    assert(isSorted([2,1]) == True)
    assert(isSorted([2,2,2,2,2,1,1,1,1,0]) == True)
    assert(isSorted([1,1,1,1,2,2,2,2,3,3]) == True)
    assert(isSorted([1,2,1]) == False)
    assert(isSorted([1,1,2,1]) == False)
    assert(isSorted(range(10,30,3)) == True)
    assert(isSorted(range(30,10,-3)) == True)
    print('Passed!')

def testSmallestDifference():
    print('Testing smallestDifference()...', end='')
    assert(smallestDifference([]) == -1)
    assert(smallestDifference([2,3,5,9,9]) == 0)
    assert(smallestDifference([-2,-5,7,15]) == 3)
    assert(smallestDifference([19,2,83,6,27]) == 4)
    assert(smallestDifference(list(range(0, 10**3, 5)) + [42]) == 2)
    print('Passed')

def _verifyLookAndSayIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    lookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

def testLookAndSay():
    print("Testing lookAndSay()...", end="")
    assert(_verifyLookAndSayIsNondestructive() == True)
    assert(lookAndSay([]) == [])
    assert(lookAndSay([1,1,1]) ==  [(3,1)])
    assert(lookAndSay([-1,2,7]) == [(1,-1),(1,2),(1,7)])
    assert(lookAndSay([3,3,8,-10,-10,-10]) == [(2,3),(1,8),(3,-10)])
    assert(lookAndSay([3,3,8,3,3,3,3]) == [(2,3),(1,8),(4,3)])
    assert(lookAndSay([2]*5 + [5]*2) == [(5,2), (2,5)])
    assert(lookAndSay([5]*2 + [2]*5) == [(2,5), (5,2)])
    print("Passed!")

def _verifyInverseLookAndSayIsNondestructive():
    a = [(1,2), (2,3)]
    b = copy.copy(a)
    inverseLookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

def testInverseLookAndSay():
    print("Testing inverseLookAndSay()...", end="")
    assert(_verifyInverseLookAndSayIsNondestructive() == True)
    assert(inverseLookAndSay([]) == [])
    assert(inverseLookAndSay([(3,1)]) == [1,1,1])
    assert(inverseLookAndSay([(1,-1),(1,2),(1,7)]) == [-1,2,7])
    assert(inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10])
    assert(inverseLookAndSay([(5,2), (2,5)]) == [2]*5 + [5]*2)
    assert(inverseLookAndSay([(2,5), (5,2)]) == [5]*2 + [2]*5)
    print("Passed!")

def _verifyNondestructiveRemoveRepeatsIsNondestructive():
    a = [3, 5, 3, 3, 6]
    b = copy.copy(a)
    # ignore result, just checking for destructiveness here
    nondestructiveRemoveRepeats(a)
    return (a == b)

def testNondestructiveRemoveRepeats():
    print("Testing nondestructiveRemoveRepeats()", end="")
    assert(_verifyNondestructiveRemoveRepeatsIsNondestructive())
    assert(nondestructiveRemoveRepeats([1,3,5,3,3,2,1,7,5]) == [1,3,5,2,7])
    assert(nondestructiveRemoveRepeats([1,2,3,-2]) == [1,2,3,-2])
    print("Passed.")

def testDestructiveRemoveRepeats():
    print("Testing destructiveRemoveRepeats()", end="")
    a = [1,3,5,3,3,2,1,7,5]
    assert(destructiveRemoveRepeats(a) == None)
    assert(a == [1,3,5,2,7])
    b = [1,2,3,-2]
    assert(destructiveRemoveRepeats(b) == None)
    assert(b == [1,2,3,-2])
    print("Passed.")

def testVoteTallyClass():
    print('Testing VoteTally class...', end='')

    # When we create a VoteTally, we provide a list of
    # candidates whose votes we are tallying:
    vt1 = VoteTally(['Fred', 'Wilma', 'Betty'])

    # We can then add votes for the candidates
    vt1.addVotes(5, 'Fred')
    vt1.addVotes(3, 'Wilma')
    vt1.addVotes(2, 'Fred')

    # If we add votes to a non-candidate, we do so gracefully:
    assert(vt1.addVotes(3, 'Bam-Bam') == 'No such candidate as Bam-Bam')

    # And we can get the total tally of votes for each candidate
    assert(vt1.getVotes('Fred') == 7)
    assert(vt1.getVotes('Wilma') == 3)
    assert(vt1.getVotes('Betty') == 0)

    # And we can gracefully handle non-candidates
    assert(vt1.getVotes('Barney') == 'No such candidate as Barney')

    # And we can also get the overall total
    assert(vt1.getVotes('Total') == 10)

    # Here is a second VoteTally with some (but not all) of the same candidates
    vt2 = VoteTally(['Fred', 'Barney', 'Betty']) 
    vt2.addVotes(5, 'Fred')
    vt2.addVotes(2, 'Betty')
    vt2.addVotes(8, 'Betty')
    assert(vt2.getVotes('Fred') == 5)
    assert(vt2.getVotes('Wilma') == 'No such candidate as Wilma')
    assert(vt2.getVotes('Betty') == 10)
    assert(vt2.getVotes('Barney') == 0)
    assert(vt2.getVotes('Total') == 15)

    # We can combine two VoteTally objects to create a third
    # VoteTally object, which includes all the candidates from either
    # tally, and combines their totals:
    vt3 = vt1.addVoteTally(vt2)
    assert(vt1.candidates == ['Fred', 'Wilma', 'Betty']) # unchanged
    assert(vt2.candidates == ['Fred', 'Barney', 'Betty']) # ditto
    # but the new VoteTally is created with a sorted list of candidates
    # in the same order as they appear first in vt1 then vt2,
    # but with no duplicates
    assert(vt3.candidates == ['Fred', 'Wilma', 'Betty', 'Barney'])
    assert(vt3.getVotes('Fred') == 12)
    assert(vt3.getVotes('Wilma') == 3)
    assert(vt3.getVotes('Betty') == 10)
    assert(vt3.getVotes('Barney') == 0)
    assert(vt3.getVotes('Pebbles') == 'No such candidate as Pebbles')
    assert(vt3.getVotes('Total') == 25)
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testAlternatingSum()
    testMedian()
    testIsSorted()
    testSmallestDifference()
    testLookAndSay()
    testInverseLookAndSay()
    testNondestructiveRemoveRepeats()
    testDestructiveRemoveRepeats()
    testVoteTallyClass()

def main():
    cs112_s20_unit4_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
