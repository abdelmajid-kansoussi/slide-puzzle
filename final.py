import pygame, sys, random
from pygame.locals import *


WINDOWWIDTH = 640
WINDOWHEIGHT = 480

BOARDWIDTH = 4
BOARDHEIGHT = 4

GREEN = (0, 204, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (3, 54, 73)

TILESIZE = 80

XMARGIN = int((WINDOWWIDTH - TILESIZE * BOARDWIDTH)/2)
YMARGIN = int((WINDOWHEIGHT - TILESIZE * BOARDHEIGHT)/2)

FPS = 30

RIGHT = "right"
UP = "up"
DOWN = "down"
LEFT = "left"

BLANK = 0

def main():
    pygame.init()
    global DISPLAYSURF, FONT, CLOCK, NEWSURFACE, NEWRECT, RESETSURFACE, RESETRECT, SOLVERECT, SOLVESURFACE
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Slide puzzle")

    NEWSURFACE, NEWRECT = makeText("New Puzzle", WHITE, GREEN, WINDOWWIDTH - 70, WINDOWHEIGHT - 40)
    RESETSURFACE, RESETRECT = makeText("Reset", WHITE, GREEN, WINDOWWIDTH - 70, WINDOWHEIGHT - 70)     
    SOLVESURFACE, SOLVERECT = makeText("Solve", WHITE, GREEN, WINDOWWIDTH - 70, WINDOWHEIGHT - 100)     

    SOLVEDBOARD = getStartingBoard()

    board, sequence = generateNewPuzzle(100)
    allMoves = []

    while True:
        slideTo = None
        drawBoard(board)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                spotX, spotY = getClickedSpot(event.pos[0], event.pos[1])
                if spotX != None and spotY != None:
                    blankX, blankY = getBlankPosition(board)
                    if spotY == blankY + 1 and spotX == blankX:
                        slideTo = UP
                    elif spotY == blankY - 1 and spotX == blankX:
                        slideTo = DOWN
                    elif spotX == blankX - 1 and spotY == blankY:
                        slideTo = RIGHT
                    elif spotX == blankX + 1 and spotY == blankY:
                        slideTo = LEFT
                else:
                    if RESETRECT.collidepoint(event.pos):
                        resetAnimation(board, allMoves)
                        allMoves = []
                    elif NEWRECT.collidepoint(event.pos):
                        board, sequence = generateNewPuzzle(100)
                    elif SOLVERECT.collidepoint(event.pos):
                        resetAnimation(board, sequence + allMoves)
                        allMoves = []


            elif event.type == KEYUP:
                if event.key == K_UP and isValidMove(UP, board):
                    slideTo = UP
                elif event.key == K_DOWN and isValidMove(DOWN, board):
                    slideTo = DOWN
                elif event.key == K_LEFT and isValidMove(LEFT, board):
                    slideTo = LEFT
                elif event.key == K_RIGHT and isValidMove(RIGHT, board):
                    slideTo = RIGHT
            
        if slideTo:
            slideAnimation(board, slideTo, 8)
            makeMove(board, slideTo)
            allMoves.append(slideTo)

        pygame.display.update()
        CLOCK.tick(FPS)

def getClickedSpot(spotLeft, spotTop):
    for tileX in range(BOARDWIDTH):
        for tileY in range(BOARDHEIGHT):
            tileLeft, tileTop = getTileTopLeft(tileX, tileY)
            tileRect = pygame.Rect(tileLeft, tileTop, TILESIZE, TILESIZE)
            if tileRect.collidepoint(spotLeft, spotTop):
                return (tileX, tileY)
    return (None,  None)

def makeMove(board, move):
    blankX, blankY = getBlankPosition(board)
    if move == UP and blankY + 1 < BOARDHEIGHT:
        board[blankX][blankY] = board[blankX][blankY + 1]
        board[blankX][blankY + 1] = BLANK
    elif move == DOWN and blankY - 1 >= 0:
        board[blankX][blankY] = board[blankX][blankY - 1]
        board[blankX][blankY - 1] = BLANK
    elif move == RIGHT and blankX - 1 >= 0:
        board[blankX][blankY] = board[blankX - 1][blankY]
        board[blankX - 1][blankY] = BLANK
    elif move == LEFT and blankX + 1 < BOARDWIDTH:
        board[blankX][blankY] = board[blankX + 1][blankY]
        board[blankX + 1][blankY] = BLANK

def slideAnimation(board, move, animationSpeed):
    blankX, blankY = getBlankPosition(board)
    if move == UP:
        moveY = blankY + 1
        moveX = blankX
    elif move == DOWN:
        moveY = blankY - 1
        moveX = blankX
    elif move == RIGHT:
        moveX = blankX - 1
        moveY = blankY
    elif move == LEFT:
        moveX = blankX + 1
        moveY = blankY
    moveLeft, moveTop = getTileTopLeft(moveX, moveY)

    drawBoard(board)
    baseSurf = DISPLAYSURF.copy()
    pygame.draw.rect(baseSurf, BLUE, (moveLeft, moveTop, TILESIZE, TILESIZE))


    for i in range(0, TILESIZE, animationSpeed):
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if move == UP:
            drawTile(moveX, moveY, str(board[moveX][moveY]), 0, -i)
        elif move == DOWN:
            drawTile(moveX, moveY, str(board[moveX][moveY]), 0, i)
        elif move == RIGHT:
            drawTile(moveX, moveY, str(board[moveX][moveY]), i, 0)
        elif move == LEFT:
            drawTile(moveX, moveY, str(board[moveX][moveY]), -i, 0)
        pygame.display.update()
        CLOCK.tick(FPS)

def isValidMove(move, board):
    blankX, blankY = getBlankPosition(board)
    if move == UP and blankY + 1 < BOARDHEIGHT and board[blankX][blankY + 1] != BLANK:
        return True
    elif move == DOWN and blankY - 1 >= 0 and board[blankX][blankY - 1] != BLANK:
        return True
    elif move == LEFT and blankX + 1 < BOARDWIDTH and board[blankX + 1][blankY] != BLANK:
        return True
    elif move == RIGHT and blankX - 1 >= 0 and board[blankX - 1][blankY] != BLANK:
        return True
    else:
        return False


def getTileTopLeft(tileX, tileY):
    left =  XMARGIN +  tileX * TILESIZE
    top = YMARGIN + tileY * TILESIZE
    return (left, top)

def makeText(text, color, bgcolor ,left, top):
    textSurface = FONT.render(str(text), True, color, bgcolor)
    textRect = textSurface.get_rect()
    textRect.center = (left, top)
    return (textSurface, textRect)


def drawTile(tileX, tileY, number, adjX = 0, adjY = 0):
    left, top = getTileTopLeft(tileX, tileY)
    pygame.draw.rect(DISPLAYSURF, GREEN, (left + adjX, top + adjY, TILESIZE, TILESIZE))
    pygame.draw.rect(DISPLAYSURF, BLUE, (left + adjX, top + adjY, TILESIZE, TILESIZE), 1)
    (textSurface, textRect) = makeText(number, WHITE, GREEN , left + adjX + TILESIZE / 2, top + adjY + TILESIZE / 2)
    DISPLAYSURF.blit(textSurface, textRect)


def drawBoard(board):
    DISPLAYSURF.fill(BLUE)
    for tileX in range(BOARDWIDTH):
        for tileY in range(BOARDHEIGHT):
            if board[tileX][tileY] != 0:
                drawTile(tileX, tileY, board[tileX][tileY])

    left, top = getTileTopLeft(0, 0)
    width = TILESIZE * BOARDWIDTH
    height = TILESIZE * BOARDHEIGHT
    pygame.draw.rect(DISPLAYSURF, WHITE, (left - 5, top - 5, width + 10, height + 10), 4)

    DISPLAYSURF.blit(NEWSURFACE, NEWRECT)
    DISPLAYSURF.blit(RESETSURFACE, RESETRECT)
    DISPLAYSURF.blit(SOLVESURFACE, SOLVERECT)

def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)

def getStartingBoard():
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(y * BOARDHEIGHT + x + 1)
        board.append(column)
    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board

def generateNewPuzzle(numSlides):
    board = getStartingBoard()
    drawBoard(board)
    pygame.display.update()
    pygame.time.wait(1000)
    sequence = []
    for t in range(numSlides):
        move = getRandomMove(board)
        slideAnimation(board, move, 30)
        makeMove(board, move)
        sequence.append(move)
    return (board, sequence)

def getRandomMove(board):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    if not isValidMove(UP, board):
        validMoves.remove(UP)
    if not isValidMove(RIGHT, board):
        validMoves.remove(RIGHT)
    if not isValidMove(DOWN, board):
        validMoves.remove(DOWN)
    if not isValidMove(LEFT, board):
        validMoves.remove(LEFT)
    return random.choice(validMoves)

def resetAnimation(board, allMoves):
    allMoves.reverse()
    for move in allMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, 30)
        makeMove(board, oppositeMove)


main()
