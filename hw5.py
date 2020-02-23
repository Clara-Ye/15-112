#################################################
# hw5.py
#
# Your name: Clara Ye
# Your andrew id: zixuany
#################################################

import cs112_s20_unit5_linter
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

class CokeMachine(object):

    # a CokeMachine object has properties bottles (number of bottles in it),
    # price (price of each bottle), and paid (money inserted in it)
    def __init__(self, bottles, price):
        self.bottleCount = bottles
        self.bottlePrice = price
        self.paidValue = 0
    
    # returns the number of bottles in the machine:
    def getBottleCount(self):
        return self.bottleCount
    
    # returns the price of each bottle:
    def getBottleCost(self):
        return self.bottlePrice

    # returns the paid money the machine contains:
    def getPaidValue(self):
        return self.paidValue

    # checks if the machine has no bottles:
    def isEmpty(self):
        return (self.bottleCount == 0)
    
    # add the given number of bottles to the machine:
    def addBottles(self, bottlesToAdd):
        self.bottleCount += bottlesToAdd

    # returns the additional money needed to buy the next bottle:
    def stillOwe(self):
        return (self.bottlePrice - self.paidValue)

    # handles an insertion of money:
    def insert(self, money):
        if (self.isEmpty()):
            # nothing happens if the machine is empty:
            return -999
        self.paidValue += money
        if (self.paidValue < self.bottlePrice):
            # nothing happens if not paid enough money:
            return -1
        else:
            # if paid enough money, give out the bottle and return the change:
            change = self.paidValue - self.bottlePrice
            self.paidValue = 0
            self.bottleCount -= 1
            return change

# returns the row and col of a given item in a given matrix:
def matrixSearch(matrix, item):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if (matrix[row][col] == item):
                return (row, col)
    return None

# checks if a given move is a legal king's move:
def isKingsMove(currRow, currCol, nextRow, nextCol):
    return (abs(nextRow - currRow) <= 1) and (abs(nextCol - currCol) <= 1)

# checks if a king can legally move over a given board in the given order:
def isKingsTour(board):
    dim = len(board)
    for i in range(1, dim**2):
        currLocation = matrixSearch(board, i)
        nextLocation = matrixSearch(board, i+1)
        # check if can successfully move:
        if (currLocation == None) or (nextLocation == None):
            return False
        (currRow, currCol) = currLocation
        (nextRow, nextCol) = nextLocation
        # check if move is legal:
        if (isKingsMove(currRow, currCol, nextRow, nextCol) == False):
            return False
    return True

# checks if a list of values are legal sudoku values:
def areLegalValues(values):
    legalValues = [n for n in range(len(values)+1)]
    for value in values:
        if value not in legalValues:
            return False
        elif (values.count(value) > 1) and (value != 0):
            return False
    return True

def testAreLegalValues():
    print('Testing areLegalValues()...', end='')
    assert(areLegalValues([ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]) == True)
    assert(areLegalValues([ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]) == True)
    assert(areLegalValues([ 1, 2, 3, 4, 0, 6, 7, 8, 0 ]) == True)
    assert(areLegalValues([ 1, 2, 3, 4, 0, 6, 1, 8, 0 ]) == False)
    assert(areLegalValues([ 1, 2, 3, 4, 0, 6,10, 8, 0 ]) == False)
    assert(areLegalValues([ 1, 2, 3, 4, 0, 6,10, 8, 0, 
                            9, 0, 0, 0, 0, 0, 0 ]) == True)
    print('Passed!')

# checks if the values in a given row are legal:
def isLegalRow(board, row):
    return areLegalValues(board[row])

# checks if the values in a given col are legal:
def isLegalCol(board, col):
    colValues = []
    for row in board:
        colValues.append(row[col])
    return areLegalValues(colValues)

# gets the values in a given block:
def getBlock(board, block):
    dim = roundHalfUp(len(board)**0.5)
    result = []
    for row in range(dim):
        for col in range(dim):
            blockRow = ((block // dim) * dim) + row
            blockCol = ((block % dim) * dim) + col
            result.append(board[blockRow][blockCol])
    return result

def testGetBlock():
    print('Testing getBlock()...', end='')    
    board = [[ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
             [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
             [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
             [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
             [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
             [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
             [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
             [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
             [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]]
    assert(getBlock(board, 0) == [5, 3, 0, 6, 0, 0, 0, 9, 8])
    assert(getBlock(board, 1) == [0, 7, 0, 1, 9, 5, 0, 0, 0])
    assert(getBlock(board, 2) == [0, 0, 0, 0, 0, 0, 0, 6, 0])
    assert(getBlock(board, 5) == [0, 0, 3, 0, 0, 1, 0, 0, 6])
    assert(getBlock(board, 7) == [0, 0, 0, 4, 1, 9, 0, 8, 0])
    print("Passed!")

# checks if the values in a given block are legal:
def isLegalBlock(board, block):
    blockValues = getBlock(board, block)
    return areLegalValues(blockValues)

# checks if a sudoku is legal:
def isLegalSudoku(board):
    for i in range(len(board)):
        if (isLegalRow(board, i) == False):
            return False
        elif (isLegalCol(board, i) == False):
            return False
        elif (isLegalBlock(board, i) == False):
            return False
    return True

### Unfinished: playSimplifiedChess()
# from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing:
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing:
def print2dList(a):
    if (a == []):
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print(" ]")

def isKnightsMove(currRow, currCol, nextRow, nextCol):
    diffRow = abs(nextRow - currRow)
    diffCol = abs(nextCol - currCol)
    return (diffRow == 1 and diffCol == 2) or (diffRow == 2 and diffCol == 1)

def isLegalMove(currRow, currCol, nextRow, nextCol, chess):
    if (chess == "K") or (chess == "k"):
        return isKingsMove(currRow, currCol, nextRow, nextCol)
    elif (chess == "Q") or (chess == "q"):
        return isQueensMove(currRow, currCol, nextRow, nextCol)
    elif (chess == "R") or (chess == "r"):
        return isRooksMove(currRow, currCol, nextRow, nextCol)
    elif (chess == "B") or (chess == "b"):
        return isBishopsMove(currRow, currCol, nextRow, nextCol)
    elif (chess == "N") or (chess == "n"):
        return isKnightsMove(currRow, currCol, nextRow, nextCol)
    elif (chess == "P") or (chess == "p"):
        return isPawnsMove(currRow, currCol, nextRow, nextCol)

def getStart(player, board):
    print(f"Player {player}, please select a chess: ")
    currRow = input("Select a row: ")
    while (not currRow.isdigit()) or (int(currRow) < 1) or (int(currRow) > 7):
        print("Illegal input. Please enter a number between 1-7.")
        currRow = input("Select a row: ")
    currRow = int(currRow)
    currCol = input("Select a column: ")
    while (not currCol.isdigit()) or (int(currCol) < 1) or (int(currCol) > 8):
        print("Illegal input. Please enter a number between 1-8.")
        currCol = input("Select a column: ")
    currCol = int(currCol)
    chess = board[currRow][currCol]
    return (currRow, currCol, chess)

def getEnd():
    print(f"Please select a grid to move to: ")
    nextRow = input("Select a row: ")
    while (not nextRow.isdigit()) or (int(nextRow) < 1) or (int(nextRow) > 7):
        print("Illegal input. Please enter a number between 1-7.")
    nextRow = int(nextRow)
    nextCol = input("Select a column: ")
    while (not nextCol.isdigit()) or (int(nextCol) < 1) or (int(nextCol) > 8):
        print("Illegal input. Please enter a number between 1-8.")
    nextCol = int(nextCol)
    return (nextRow, nextCol)

def playRound(player, board):
    print2dList(board)
    (currRow, currCol, chess) = getStart(player, board)
    while (chess == " "):
        print("There is no chess in the grid.")
        print("Please select a grid with a chess.")
        (currRow, currCol, chess) = getStart(player, board)
    while (((player == 1) and (chess.islower())) or
           ((player == 2) and (chess.isupper()))):
        print("You cannot move your opponent's chess.")
        print("Please select another chess.")
        (currRow, currCol, chess) = getStart(player, board)
    (nextRow, nextCol) = getEnd()
    while (not isLegalMove(currRow, currCol, nextRow, nextCol, chess)):
        print(f"Illegal move for {chess}. Please select another move.")
        print("Enter H for help.")
        playRound(player, board)
        break
    board[currRow][currCol] = " "
    board[nextRow][nextCol] = chess

def isWin(board):
    if ((matrixSearch(board, "k") == None) or 
        (matrixSearch(board, "K") == None)):
        return True
    return False

def playSimplifiedChess():
    board = [[" ", "1", "2", "3", "4", "5", "6", "7", "8"],
             ["1", "R", "N", "B", "K", "Q", "B", "N", "R"],
             ["2", "P", "P", "P", "P", "P", "P", "P", "P"],
             ["3", " ", " ", " ", " ", " ", " ", " ", " "],
             ["4", " ", " ", " ", " ", " ", " ", " ", " "],
             ["5", " ", " ", " ", " ", " ", " ", " ", " "],
             ["6", "p", "p", "p", "p", "p", "p", "p", "p"],
             ["7", "r", "n", "b", "k", "q", "b", "n", "r"]]
    while (isWin(board) == False):
        playRound(1, board)
        if isWin(board):
            print("Player 1 wins!")
            break
        playRound(2, board)
        if isWin(board):
            print("Player 2 wins!")
            break

#################################################
# Test Functions
#################################################

def testCokeMachineClass():
    print('Testing CokeMachine class...', end='')
    cm1 = CokeMachine(100, 125) # make a CokeMachine holding 100 bottles
                                # that each cost 125 cents ($1.25)
    assert(cm1.getBottleCount() == 100)
    assert(cm1.isEmpty() == False)
    assert(cm1.getBottleCost() == 125)  # $1.25 (125 cents)
    assert(cm1.getPaidValue() == 0)     # starts with no coins inserted

    # insert a dollar
    change = cm1.insert(100)  # we paid $1.00, it costs $1.25, so change == -1
                              # to indicate that not only is there no change,
                              # but we still owe money
    assert(change == -1)
    assert(cm1.stillOwe() == 25)

    # insert a dime more
    change = cm1.insert(10)
    assert(change == -1)
    assert(cm1.stillOwe() == 15)

    # and insert a quarter more.  Here, we finally pay enough, so we get a
    # bottle and some change!
    change = cm1.insert(25)
    assert(change == 10)
    assert(cm1.stillOwe() == 125)      # this is for the NEXT bottle
    assert(cm1.getBottleCount() == 99) # because we just got one!

    # second instance
    cm2 = CokeMachine(2, 50) # 2 bottles, $0.50 each

    # buy a couple bottles
    change = cm2.insert(25)
    assert(change == -1)
    assert(cm2.stillOwe() == 25)
    change = cm2.insert(25)
    assert(change == 0) # bought with exact change
    assert(cm2.isEmpty() == False)
    assert(cm2.getBottleCount() == 1)
    change = cm2.insert(100) # overpaid by $0.50
    assert(change == 50)
    assert(cm2.isEmpty() == True)
    assert(cm2.getBottleCount() == 0)

    # cannot buy anything more -- the machine is empty.
    # this is signified by returning -999 as the change
    change = cm2.insert(50)
    assert(change == -999)
    assert(cm2.isEmpty() == True)
    assert(cm2.getBottleCount() == 0)

    # addBottles method
    cm2.addBottles(50)
    assert(cm2.isEmpty() == False)
    assert(cm2.getBottleCount() == 50)
    change = cm2.insert(50)
    assert(change == 0)
    assert(cm2.getBottleCount() == 49)

    # independence of two instances
    assert(cm1.getBottleCount() == 99)
    assert(cm2.getBottleCount() == 49)

    print('Passed')

def testIsKingsTour():
    print("Testing isKingsTour()...", end="")
    a = [ [  3, 2, 1 ],
          [  6, 4, 9 ],
          [  5, 7, 8 ] ]
    assert(isKingsTour(a) == True)
    a = [ [  2, 8, 9 ],
          [  3, 1, 7 ],
          [  4, 5, 6 ] ]
    assert(isKingsTour(a) == True)
    a = [ [  7, 5, 4 ],
          [  6, 8, 3 ],
          [  1, 2, 9 ] ]
    assert(isKingsTour(a) == True)
    a = [ [  7, 5, 4 ],
          [  6, 8, 3 ],
          [  1, 2, 1 ] ]
    assert(isKingsTour(a) == False)
    a = [ [  3, 2, 9 ],
          [  6, 4, 1 ],
          [  5, 7, 8 ] ]
    assert(isKingsTour(a) == False)
    a = [ [  3, 2, 1 ],
          [  6, 4, 0 ],
          [  5, 7, 8 ] ]
    assert(isKingsTour(a) == False)
    a = [ [  1, 2, 3 ],
          [  7, 4, 8 ],
          [  6, 5, 9 ] ]
    assert(isKingsTour(a) == False)
    a = [ [ 3, 2, 1 ],
          [ 6, 4, 0 ],
          [ 5, 7, 8 ] ]
    assert(isKingsTour(a) == False)
    print("Passed!")

def testIsLegalSudoku():
    # From Leon Zhang!
    print("Testing isLegalSudoku()...", end="")
    board = [[0]]
    assert isLegalSudoku(board) == True
    board = [[1]]
    assert isLegalSudoku(board) == True

    board = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
    assert isLegalSudoku(board) == True
    board = [[0, 4, 0, 0],
             [0, 0, 3, 0],
             [1, 0, 0, 0],
             [0, 0, 0, 2]]
    assert isLegalSudoku(board) == True
    board = [[1, 2, 3, 4],
             [3, 4, 1, 2],
             [2, 1, 4, 3],
             [4, 3, 2, 1]]
    assert isLegalSudoku(board) == True
    board = [[1, 2, 3, 4],
             [3, 4, 4, 2],
             [2, 4, 4, 3],
             [4, 3, 2, 1]]    
    assert isLegalSudoku(board) == False

    board = [
    [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
    [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
    [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
    [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
    [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
    [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
    [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
    [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
    [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
    ]
    assert isLegalSudoku(board) == True
    
    board = [
    [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
    [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
    [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
    [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
    [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
    [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
    [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
    [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
    [ 0, 0, 0, 0, 8, 0, 9, 7, 9 ]
    ]
    assert isLegalSudoku(board) == False
    board = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert isLegalSudoku(board) == True
    board = [
    [ 2,11, 9, 5, 8,16,13, 4,12, 3,14, 7,10, 6,15, 1],
    [ 4,12,15,10, 3, 6, 9,11,13, 5, 8, 1,16, 7,14, 2],
    [ 1,14, 6, 7,15, 2, 5,12,11, 9,10,16, 3,13, 8, 4],
    [16,13, 8, 3,14, 1,10, 7, 4, 6, 2,15, 9,11, 5,12],
    [12, 2,16, 9,10,14,15,13, 8, 1, 5, 3, 6, 4,11, 7],
    [ 6, 7, 1,11, 5,12, 8,16, 9,15, 4, 2,14,10, 3,13],
    [14, 5, 4,13, 6,11, 1, 3,16,12, 7,10, 8, 9, 2,15],
    [ 3, 8,10,15, 4, 7, 2, 9, 6,14,13,11, 1,12,16, 5],
    [13, 9, 2,16, 7, 8,14,10, 3, 4,15, 6,12, 5, 1,11],
    [ 5, 4,14, 6, 2,13,12, 1,10,16,11, 8,15, 3, 7, 9],
    [ 7, 1,11,12,16, 4, 3,15, 5,13, 9,14, 2, 8,10, 6],
    [10,15, 3, 8, 9, 5,11, 6, 2, 7, 1,12, 4,14,13,16],
    [11,10,13,14, 1, 9, 7, 8,15, 2, 6, 4, 5,16,12, 3],
    [15, 3, 7, 4,12,10, 6, 5, 1, 8,16,13,11, 2, 9,14],
    [ 8, 6, 5, 1,13, 3,16, 2,14,11,12, 9, 7,15, 4,10],
    [ 9,16,12, 2,11,15, 4,14, 7,10, 3, 5,13, 1, 6, 8]]
    assert isLegalSudoku(board) == True
    # last number is supposed to be 8, not 10
    board = [
    [ 2,11, 9, 5, 8,16,13, 4,12, 3,14, 7,10, 6,15, 1],
    [ 4,12,15,10, 3, 6, 9,11,13, 5, 8, 1,16, 7,14, 2],
    [ 1,14, 6, 7,15, 2, 5,12,11, 9,10,16, 3,13, 8, 4],
    [16,13, 8, 3,14, 1,10, 7, 4, 6, 2,15, 9,11, 5,12],
    [12, 2,16, 9,10,14,15,13, 8, 1, 5, 3, 6, 4,11, 7],
    [ 6, 7, 1,11, 5,12, 8,16, 9,15, 4, 2,14,10, 3,13],
    [14, 5, 4,13, 6,11, 1, 3,16,12, 7,10, 8, 9, 2,15],
    [ 3, 8,10,15, 4, 7, 2, 9, 6,14,13,11, 1,12,16, 5],
    [13, 9, 2,16, 7, 8,14,10, 3, 4,15, 6,12, 5, 1,11],
    [ 5, 4,14, 6, 2,13,12, 1,10,16,11, 8,15, 3, 7, 9],
    [ 7, 1,11,12,16, 4, 3,15, 5,13, 9,14, 2, 8,10, 6],
    [10,15, 3, 8, 9, 5,11, 6, 2, 7, 1,12, 4,14,13,16],
    [11,10,13,14, 1, 9, 7, 8,15, 2, 6, 4, 5,16,12, 3],
    [15, 3, 7, 4,12,10, 6, 5, 1, 8,16,13,11, 2, 9,14],
    [ 8, 6, 5, 1,13, 3,16, 2,14,11,12, 9, 7,15, 4,10],
    [ 9,16,12, 2,11,15, 4,14, 7,10, 3, 5,13, 1, 6,10]]
    assert isLegalSudoku(board) == False
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    # required
    testCokeMachineClass()

    # mild
    testIsKingsTour()

    # medium
    testAreLegalValues()
    testGetBlock()
    testIsLegalSudoku()

    # spicy
    # Note that playSimplifiedChess is manually graded
    # so there is no test function for it.
    playSimplifiedChess()

def main():
    cs112_s20_unit5_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
