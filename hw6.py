#################################################
# hw6.py: Tetris!
#
# Your name: Clara Ye
# Your andrew id: zixuany
#
# Your partner's name: Linpeng Chen
# Your partner's andrew id: linpengc
#################################################

import cs112_s20_unit6_linter
import math, copy, random

from cmu_112_graphics import *

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

# initialize variables:
def appStarted(app):
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions()
    app.emptyColor = "blue"
    app.board = make2DList(app.rows, app.cols, app.emptyColor)
    app.score = 0
    app.timerDelay = 250
    app.gameOver = False
    # initialize the falling pieces:
    app.iPiece = [[  True,  True,  True,  True ]]
    app.jPiece = [[  True, False, False ],
                  [  True,  True,  True ]]
    app.lPiece = [[ False, False,  True ],
                  [  True,  True,  True ]]
    app.oPiece = [[  True,  True ],
                  [  True,  True ]]
    app.sPiece = [[ False,  True,  True ],
                  [  True,  True, False ]]
    app.tPiece = [[ False,  True, False ],
                  [  True,  True,  True ]]
    app.zPiece = [[  True,  True, False ],
                  [ False,  True,  True ]]
    app.tetrisPieces = [ app.iPiece, app.jPiece, app.lPiece, app.oPiece, 
                         app.sPiece, app.tPiece, app.zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", 
                              "green", "orange" ]
    # place the first falling piece:
    newFallingPiece(app)

# makes a 2d list with given dimentions and filler item:
def make2DList(rows, cols, filler):
    return [[filler]*cols for row in range(rows)]

# generates a random falling piece:
def newFallingPiece(app):
    # get the shape:
    fallingPieceIndex = random.randint(0, len(app.tetrisPieces)-1)
    app.fallingPiece = app.tetrisPieces[fallingPieceIndex]
    # get the color:
    fallingColorIndex = random.randint(0, len(app.tetrisPieceColors) - 1)
    app.fallingPieceColor = app.tetrisPieceColors[fallingColorIndex]
    # place the falling piece in the top-middle of the board:
    app.fallingPieceRow = 0
    app.fallingPieceCol = (app.cols // 2) - (len(app.fallingPiece[0]) // 2)

# handles keypress events:
def keyPressed(app, event):
    if event.key == "r": playTetris()
    elif (app.gameOver == True): return
    elif (event.key == "Left"): moveFallingPiece(app, 0, -1)
    elif (event.key == "Right"): moveFallingPiece(app, 0, +1)
    elif (event.key == "Down"): moveFallingPiece(app, +1, 0)
    elif (event.key == "Up"): rotateFallingPiece(app)
    elif (event.key == "Space"): hardDrop(app)

# runs features that continuously change as time passes:
def timerFired(app):
    if (app.gameOver == True): return
    elif (not fallingPieceIsLegal(app)): app.gameOver = True
    elif (not moveFallingPiece(app, +1, 0)): placeFallingPiece(app)

# checks if the falling piece is legal, e.g., on board and in empty cells:
def fallingPieceIsLegal(app):
    for pieceRow in range(len(app.fallingPiece)):
        row = pieceRow + app.fallingPieceRow
        for pieceCol in range(len(app.fallingPiece[0])):
            col = pieceCol + app.fallingPieceCol
            if (app.fallingPiece[pieceRow][pieceCol] == True):
                if ((row not in range(len(app.board))) or 
                    (col not in range(len(app.board[0]))) or
                    (app.board[row][col] != app.emptyColor)):
                    return False
    return True

# moves the falling piece by one cell in the given direction:
def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    return True

# moves the falling pieces downwards as far as possible:
def hardDrop(app):
    while moveFallingPiece(app, 1, 0):
        continue

# rotates the falling conterclockwise:
def rotateFallingPiece(app):
    # store old variables:
    oldPiece = app.fallingPiece
    (oldRows, oldCols) = (len(app.fallingPiece), len(app.fallingPiece[0]))
    # rotate the piece:
    app.fallingPiece = make2DList(oldCols, oldRows, None)
    for row in range(oldRows):
        for col in range(oldCols):
            app.fallingPiece[col][row] = oldPiece[row][oldCols-1-col]
    # adjust the location:
    (oldRow, oldCol) = (app.fallingPieceRow, app.fallingPieceCol)
    app.fallingPieceRow = oldRow + oldRows//2 - len(app.fallingPiece)//2
    app.fallingPieceCol = oldCol + oldCols//2 - len(app.fallingPiece[0])//2
    # check if new position is legal:
    if not fallingPieceIsLegal(app):
        app.fallingPiece = oldPiece
        app.fallingPieceRow = oldRow
        app.fallingPieceCol = oldCol

# updates the board so the falling piece is placed on the board:
def placeFallingPiece(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col]:
                boardRow = app.fallingPieceRow + row
                boardCol = app.fallingPieceCol + col
                app.board[boardRow][boardCol] = app.fallingPieceColor
    removeFullRows(app)
    newFallingPiece(app)

# removes all the full rows on the board:
def removeFullRows(app):
    # copy all the non-full board to a separate board:
    newBoard = []
    for row in range(app.rows-1, -1, -1):
        if app.emptyColor in app.board[row]:
            newBoard.insert(0, app.board[row])
    # update the score:
    app.score += (app.rows - len(newBoard))**2
    # fill the remaining rows with empty color:
    while (len(newBoard) < app.rows):
        newBoard.insert(0, [app.emptyColor for col in range(app.cols)])
    app.board = newBoard

# updates the view:
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "orange")
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    if app.gameOver: drawGameOver(app, canvas)

# draws the board:
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

# draws a single cell:
def drawCell(app, canvas, row, col, color):
    x1 = app.margin + (app.cellSize * col)
    x2 = app.margin + (app.cellSize * (col+1))
    y1 = app.margin + (app.cellSize * row)
    y2 = app.margin + (app.cellSize * (row+1))
    canvas.create_rectangle(x1, y1, x2, y2, width = 4, fill = color)

# draws the falling piece:
def drawFallingPiece(app, canvas):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col]:
                drawCell(app, canvas, row + app.fallingPieceRow, 
                         col+app.fallingPieceCol, app.fallingPieceColor)

# draws the score display:
def drawScore(app, canvas):
    canvas.create_text(app.width//2, app.margin//2, fill = "blue",
                       text = f"Score: {app.score}", font = "Arial 10 bold")

# draws the game over message:
def drawGameOver(app, canvas):
    canvas.create_rectangle(0, (app.height//2 - app.cellSize*1.5),
                            app.width, (app.height//2 + app.cellSize*1.5),
                            fill = "black")
    canvas.create_text(app.width//2, app.height//2, text = "Game Over",
                       fill = "yellow", font = "Arial 28 bold")

# sets game dimensions:
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

# starts a tetris game:
def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    windowWidth = (cols*cellSize) + (margin*2)
    windowHeight = (rows*cellSize) + (margin*2)
    runApp(width = windowWidth, height = windowHeight)
    
#################################################
# main
#################################################

def main():
    cs112_s20_unit6_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
