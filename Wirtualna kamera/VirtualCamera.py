import pygame
import array

pygame.init()

display_width = 900
display_heigth = 700
numberOfPoints = 24
focalLength = 200
step = 10
xd = focalLength

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

listOfX = [0] * numberOfPoints
listOfY = [0] * numberOfPoints
listOfZ = [0] * numberOfPoints
listOfLinesToDraw = []

def moveRight():
    for x in range(0, numberOfPoints):
        listOfX[x] = listOfX[x] + step

def moveLeft():
    for x in range(0, numberOfPoints):
        listOfX[x] = listOfX[x] - step

def moveUp():
    for x in range(0, numberOfPoints):
        listOfY[x] = listOfY[x] - step

def moveDown():
    for x in range(0, numberOfPoints):
        listOfY[x] = listOfY[x] + step

def moveForward():
    for x in range(0, numberOfPoints):
        listOfZ[x] = listOfZ[x] - step

def moveBackward():
    for x in range(0, numberOfPoints):
        listOfZ[x] = listOfZ[x] + step

def zoomIn():
    global focalLength
    focalLength = focalLength + step

def zoomOut():
    global focalLength
    focalLength = focalLength - step



def makeLine2D(x1, y1, z1, x2, y2, z2):
    if z1 > 1:
        x3 = x1 * focalLength / z1
        y3 = y1 * focalLength / z1
    else:
        x3 = x1 * focalLength
        y3 = y1 * focalLength
    if z2 > 1:
        x4 = x2 * focalLength / z2
        y4 = y2 * focalLength / z2
    else:
        x4 = x2 * focalLength
        y4 = y2 * focalLength
    listOfLinesToDraw.append(x3)
    listOfLinesToDraw.append(y3)
    listOfLinesToDraw.append(x4)
    listOfLinesToDraw.append(y4)

def drawLines(linesToDraw):
    for x in range(0, len(linesToDraw), 4):
        node_1 = [linesToDraw[x], linesToDraw[x + 1]]
        node_2 = [linesToDraw[x + 2], linesToDraw[x + 3]]
        pygame.draw.line(cameraDisplay, white, (node_1), (node_2))

def centerLines(linesToDraw):
    for x in range(0, len(linesToDraw), 2):
        linesToDraw[x] = linesToDraw[x] + display_width / 2
    for x in range(1, len(linesToDraw), 2):
        linesToDraw[x] = linesToDraw[x] + display_heigth / 2


cameraDisplay = pygame.display.set_mode((display_width,display_heigth))


def cameraConf():

    with open('points.txt') as f:
        points = [[int(x) for x in line.split()] for line in f]

    k = 0
    for i in range(0, 12):
        for j in range(0, 6, 3):
            listOfX[k] = points[i][j]
            k = k + 1

    k = 0
    for i in range(0, 12):
        for j in range(1, 6, 3):
            listOfY[k] = points[i][j]
            k = k + 1

    k = 0
    for i in range(0, 12):
        for j in range(2, 6, 3):
            listOfZ[k] = points[i][j]
            k = k + 1
    print(listOfX)
    print(listOfY)
    print(listOfZ)
    print(len(listOfX))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveLeft()
                elif event.key == pygame.K_RIGHT:
                    moveRight()
                elif event.key == pygame.K_UP:
                    moveUp()
                elif event.key == pygame.K_DOWN:
                    moveDown()
                elif event.key == pygame.K_w:
                    zoomIn()
                elif event.key == pygame.K_s:
                    zoomOut()
                elif event.key == pygame.K_f:
                    moveForward()
                elif event.key == pygame.K_b:
                    moveBackward()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    y_move = 5
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    y_move = 2
                    #currentMove = 0

        cameraDisplay.fill(black)
        listOfLinesToDraw.clear()
        for x in range(0, (len(listOfX)), 2):
            makeLine2D(listOfX[x], listOfY[x], listOfZ[x], listOfX[x+1], listOfY[x+1], listOfZ[x+1])
        centerLines(listOfLinesToDraw)
        drawLines(listOfLinesToDraw)
        pygame.display.update()


cameraConf()