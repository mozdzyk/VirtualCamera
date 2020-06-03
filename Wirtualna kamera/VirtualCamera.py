import pygame
import math

pygame.init()

display_width = 900
display_height = 700
numberOfPoints = 2 * 78
startingFocalLength = 200
step = 3
degree2 = 0.005

focalLength = startingFocalLength
white = (255, 255, 255)
black = (0, 0, 0)

listOfX = [0] * numberOfPoints
listOfY = [0] * numberOfPoints
listOfZ = [0] * numberOfPoints
listOfLinesToDraw = []


def updateCoordinates(addX, addY, addZ, addFocalLength, addRotateX, addRotateY, addRotateZ):
    global focalLength
    focalLength = focalLength + addFocalLength
    if focalLength < startingFocalLength:
        focalLength = startingFocalLength
    for x in range(0, numberOfPoints):
        listOfX[x] = listOfX[x] + addX
        listOfX[x] = math.cos(addRotateY) * listOfX[x] + math.sin(addRotateY) * listOfZ[x]
        listOfX[x] = math.cos(addRotateZ) * listOfX[x] - math.sin(addRotateZ) * listOfY[x]
    for x in range(0, numberOfPoints):
        listOfY[x] = listOfY[x] + addY
        listOfY[x] = listOfY[x] * math.cos(addRotateX) + listOfZ[x] * -math.sin(addRotateX)
        listOfY[x] = listOfX[x] * math.sin(addRotateZ) + listOfY[x] * math.cos(addRotateZ)
    for x in range(0, numberOfPoints):
        listOfZ[x] = listOfZ[x] + addZ
        listOfZ[x] = -math.sin(addRotateY) * listOfX[x] + math.cos(addRotateY) * listOfZ[x]
        listOfZ[x] = math.sin(addRotateX) * listOfY[x] + math.cos(addRotateX) * listOfZ[x]


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
        pygame.draw.line(cameraDisplay, white, node_1, node_2)


def centerLines(linesToDraw):
    for x in range(0, len(linesToDraw), 2):
        linesToDraw[x] = linesToDraw[x] + display_width / 2
    for x in range(1, len(linesToDraw), 2):
        linesToDraw[x] = linesToDraw[x] + display_height / 2


def cameraConf():
    addFocalLength = 0
    addX = 0
    addY = 0
    addZ = 0
    addRotateX = 0
    addRotateY = 0
    addRotateZ = 0
    global focalLength
    with open('points.txt') as f:
        points = [[int(x) for x in line.split()] for line in f]

    k = 0
    for i in range(0, int(numberOfPoints / 2)):
        for j in range(0, 6, 3):
            listOfX[k] = points[i][j]
            k = k + 1

    k = 0
    for i in range(0, int(numberOfPoints / 2)):
        for j in range(1, 6, 3):
            listOfY[k] = points[i][j]
            k = k + 1

    k = 0
    for i in range(0, int(numberOfPoints / 2)):
        for j in range(2, 6, 3):
            listOfZ[k] = points[i][j]
            k = k + 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # move left
                    addX = step
                elif event.key == pygame.K_RIGHT:  # move right
                    addX = -step
                elif event.key == pygame.K_UP:  # move forward
                    addZ = -step
                elif event.key == pygame.K_DOWN:  # move backward
                    addZ = step
                elif event.key == pygame.K_SLASH:  # zoom in
                    addFocalLength = step
                elif event.key == pygame.K_COMMA:  # zoom out
                    addFocalLength = -step
                elif event.key == pygame.K_w:  # move up
                    addY = step
                elif event.key == pygame.K_s:  # move down
                    addY = -step
                elif event.key == pygame.K_z:  # rotate Y left
                    addRotateY = degree2
                elif event.key == pygame.K_x:  # rotate Y right
                    addRotateY = -degree2
                elif event.key == pygame.K_c:  # rotate X up
                    addRotateX = -degree2
                elif event.key == pygame.K_v:  # rotate X down
                    addRotateX = degree2
                elif event.key == pygame.K_b:  # rotate Z left
                    addRotateZ = -degree2
                elif event.key == pygame.K_n:  # rotate Z right
                    addRotateZ = degree2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    addX = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    addZ = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    addY = 0
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    addRotateY = 0
                elif event.key == pygame.K_c or event.key == pygame.K_v:
                    addRotateX = 0
                elif event.key == pygame.K_b or event.key == pygame.K_n:
                    addRotateZ = 0
                elif event.key == pygame.K_COMMA or event.key == pygame.K_SLASH:
                    addFocalLength = 0

        cameraDisplay.fill(black)
        listOfLinesToDraw.clear()
        updateCoordinates(addX, addY, addZ, addFocalLength, addRotateX, addRotateY, addRotateZ)
        for x in range(0, (len(listOfX)), 2):
            makeLine2D(listOfX[x], listOfY[x], listOfZ[x], listOfX[x + 1], listOfY[x + 1], listOfZ[x + 1])
        centerLines(listOfLinesToDraw)
        drawLines(listOfLinesToDraw)
        pygame.display.update()


cameraDisplay = pygame.display.set_mode((display_width, display_height))
cameraConf()
