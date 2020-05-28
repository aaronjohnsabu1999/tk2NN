## Package Import
import math
import matplotlib
import numpy as np
# import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import time
from colour import Color
from copy import deepcopy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from random import random
from statistics import multimode
from tkinter import *
from tkinter import messagebox

matplotlib.use("TkAgg")

def euDist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def mhDist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def colorInitPoints(canvasSet, pointSet):
    for point in pointSet:
        try:
            canvasSet[point[0][1]][point[0][0]] = point[1].lower()
        except Exception:
            canvasSet[point[0][1]][point[0][0]] = point[1]

def nthMinIndex(n, distances):
    temp = deepcopy(distances)
    for i in range(n):
        temp = [dist for dist in temp if not (dist == min(temp))]
    
    indices = []
    try:
        for i in range(len(distances)):
            if (distances[i] == min(temp)):
                indices.append(i)
    except Exception:
        return []
    return indices

def minK(k, distances, pointSet):
    closestK = []
    # print(distances)
    for i in range(2*k-1):
        # print(pointSet[nthMinIndex(i, distances)])
        for index in nthMinIndex(i, distances):
            closestK.append(pointSet[index][1])
    return multimode(closestK)[0]

def distDeter(distType, pointX, pointY, pointSet = []):
    distances = []
    k = 2
    for chosenPoint in pointSet:
        if distType == 1:
            distances.append(euDist(pointX, pointY, chosenPoint[0][0], chosenPoint[0][1]))
        else:
            distances.append(mhDist(pointX, pointY, chosenPoint[0][0], chosenPoint[0][1]))
    
    return minK(k, distances, pointSet)
    
## Euclidean Calculations
def canvasDetermine(distType, canvasWidth, canvasHeight, pointSet = []):
    canvasSet = [[0 for x in range(canvasWidth)] for y in range(canvasHeight)]

    # Check if any pixel dimension is zero
    if distType not in [1, 2]:
        return (canvasSet, 1)

    for y in range(0, canvasHeight):
        for x in range(0, canvasWidth):
            canvasSet[y][x] = distDeter(distType, x, y, pointSet)
    
    colorInitPoints(canvasSet, pointSet)

    return (canvasSet, 0)







## Free Draw
def addPoint(event):
    global freePoints
    x, y = event.x, event.y

    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        x = (x - x%sqSize)
        y = (y - y%sqSize)
        
        if (x, y) not in freePoints:
            freePoints.append((x, y))
        updatePointSpace()

def removePoint(event):
    global freePoints
    x, y = event.x, event.y
        
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        x = (x - x%sqSize)
        y = (y - y%sqSize)
        
        if (x, y) in freePoints:
            freePoints.remove((x, y))
        updatePointSpace()

## Line Draw
startPoint = (0.0, 0.0)

def addLineStart(event):
    global startPoint
    x, y = event.x, event.y
    
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        x = (x - x%sqSize)
        y = (y - y%sqSize)
        startPoint = (x, y)
        updatePointSpace()

def addLineEnd(event):
    global linePoints, startPoint
    x, y = event.x, event.y
    
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        x = (x - x%sqSize)
        y = (y - y%sqSize)
        endPoint = (x, y)
        if startPoint == endPoint:
            return
        duoPoint = (startPoint, endPoint)
        if duoPoint not in linePoints:
            linePoints.append(duoPoint)
        updatePointSpace()

def removeLine(event):
    global linePoints
    x, y = event.x, event.y
    
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        point = (x, y)
        for duoPoint in linePoints:
            startPoint = duoPoint[0]
            endPoint   = duoPoint[1]
            dist = abs( (point[1]-startPoint[1])*(endPoint[0]-startPoint[0]) - (point[0]-startPoint[0])*(endPoint[1]-startPoint[1]) )
            norm = ((endPoint[0]-startPoint[0])**2 + (endPoint[1]-startPoint[1])**2)**0.5
            if dist/norm < 5:
                linePoints.remove(duoPoint)
        updatePointSpace()

## Circle Draw
center = (0.0, 0.0)

def chooseCircleCenter(event):
    global center
    x, y = event.x, event.y
    
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        x = (x - x%sqSize)
        y = (y - y%sqSize)
        center = (x, y)
        updatePointSpace()

def chooseCircleRadius(event):
    global circPoints, center
    x, y = event.x, event.y
    
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        x = (x - x%sqSize)
        y = (y - y%sqSize)
        outerP = (x, y)
        if center == outerP:
            return
        duoPoint = (center, outerP)
        if duoPoint not in circPoints:
            circPoints.append(duoPoint)
        updatePointSpace()

def removeCircle(event):
    global circPoints
    x, y = event.x, event.y
    
    if (x >= 0 and y >= 0) and (x <= BORDER_XH - BORDER_XL and y <= BORDER_YH - BORDER_YL):
        point = (x, y)
        for duoPoint in circPoints:
            center = duoPoint[0]
            outerP   = duoPoint[1]
            dist = ((center[0]-point [0])**2 + (center[1]-point [1])**2)**0.5
            rad  = ((center[0]-outerP[0])**2 + (center[1]-outerP[1])**2)**0.5
            if abs(dist/rad - 1) < 0.02:
                circPoints.remove(duoPoint)
        updatePointSpace()

## General Space Commands
def clearPointSpace(event):
    global freePoints
    freePoints = []
    pointSpace.delete(ALL)

def updatePointSpace():
    global freePoints, linePoints
    pointSpace.delete(ALL)
    for point in freePoints:
        pointSpace.create_polygon((point[0], point[1], point[0]+sqSize, point[1], point[0]+sqSize, point[1]+sqSize, point[0], point[1]+sqSize), fill = 'white')
    for duoPoint in linePoints:
        point1 = duoPoint[0]
        point2 = duoPoint[1]
        pointSpace.create_line(point1[0]+2, point1[1]+2, point2[0]+2, point2[1]+2, width = int(sqSize / 2 + 1), fill = 'white')
    for duoPoint in circPoints:
        center = duoPoint[0]
        outerP = duoPoint[1]
        rad    = ((center[0]-outerP[0])**2 + (center[1]-outerP[1])**2)**0.5
        pointSpace.create_oval(center[0]-rad, center[1]-rad, center[0]+rad, center[1]+rad, width = int(sqSize / 2 + 1), outline = 'white')

## Output Generation
def updateOutput(event):
    global image1, draw, freePoints, fileName, fileFormat

    image1 = PIL.Image.new("RGB", (BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL))
    draw   = PIL.ImageDraw.Draw(image1)
    for duoPoint in circPoints:
        center = duoPoint[0]
        outerP = duoPoint[1]
        rad    = ((center[0]-outerP[0])**2 + (center[1]-outerP[1])**2)**0.5
        radSt  = rad - int(sqSize / 2 + 1)
        draw.ellipse([center[0]-rad,   center[1]-rad,   center[0]+rad,   center[1]+rad],   'white')
        draw.ellipse([center[0]-radSt, center[1]-radSt, center[0]+radSt, center[1]+radSt], 'black')
    for point in freePoints:
        draw.polygon([point[0], point[1], point[0]+sqSize, point[1], point[0]+sqSize, point[1]+sqSize, point[0], point[1]+sqSize],fill='white')
    for duoPoint in linePoints:
        point1 = duoPoint[0]
        point2 = duoPoint[1]
        draw.line([point1[0]+2, point1[1]+2, point2[0]+2, point2[1]+2], 'white', int(sqSize / 2 + 1))
    

    fileName = FName.get()
    fileFormat = FForm.get()
    if fileName == "":
        messagebox.showinfo("Error", "File name cannot be empty")
        return
    if fileFormat == "":
        messagebox.showinfo("Error", "File format cannot be empty")
        return
    try:
        image1.save(str(fileName) + "." + str(fileFormat))
    except Exception as e:
        if (str(e) == "unknown file extension: ." + str(fileFormat)):
            messagebox.showinfo("Error", "." + str(fileFormat) + " is an unknown image format")
        else:
            messagebox.showinfo("Error", str(e))
        return


def colorPicker(pointSet = []):
    choiceSet = {}
    for point in pointSet:
        if not point[1] in choiceSet:
            choiceSet[point[1]] = Color(rgb=(random(), random(), random()))
    return choiceSet

def bindButtons():
    pointSpace.delete("all")
    updateCanvas()

def updateCanvas():
    (canvas, error) = canvasDetermine(distType.get(), BORDER_XH - BORDER_XL, BORDER_YH - BORDER_YL, selectPoints)
    colors          = colorPicker(selectPoints)

    resolution = 1
    for y in range(resolution, BORDER_YH - BORDER_YL + resolution, resolution*2):
        for x in range(resolution, BORDER_XH - BORDER_XL + resolution, resolution*2):
            color = colors[canvas[y][x]]
            color.saturation = (color.saturation + 1.0)/2.0
            pointSpace.create_rectangle(x - resolution, y - resolution, x + resolution, y + resolution, fill = color)
    for point in selectPoints:
        pointX, pointY = point[0]
        pointSpace.create_rectangle(pointX - resolution*2, pointY - resolution*2, pointX + resolution*2, pointY + resolution*2, fill = colors[point[1]])


## App Space Variables
HEIGHT     = 500
WIDTH      = 500
fileName   = "image"
fileFormat = "png" 

## Point Space Variables
sqSize     =   4
BORDER_XL  =  50
BORDER_YL  =  50
BORDER_XH  = 450
BORDER_YH  = 350
freePoints = []
linePoints = []
circPoints = []


## Root Definition
base   = Tk()
base.resizable(width = False, height = False)
base.title("tk2NN")
base.configure(bg = 'grey')
base.geometry(str(HEIGHT) + "x" + str(WIDTH))


## Root-based Variables
distType = IntVar()
distType.set(1)

# background_image = PhotoImage(file = './background_01.png')
# background_label = Label(base, image = background_image)
# background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

selectPoints    = [
                ((251, 234), 0),
                ((180,  45), 1),
                ((203,  50), 2),
                (( 38, 231), 1),
                ((386, 182), 3),
                ((143, 234), 0),
                ((315, 178), 3),
                ((280, 264), 2),
                ((313, 114), 1),
                ((229, 122), 2),
                ]

## Space Definitions
pointSpace = Canvas(base, width = BORDER_XH - BORDER_XL, height = BORDER_YH - BORDER_YL, borderwidth = 4, relief = SUNKEN, background = 'black', cursor = 'dot')
pointSpace.grid(row = 0, column = 0, columnspan = 3, padx = (BORDER_XL, 5), pady = (BORDER_YL, 5))
pointSpace.bind("<Button-2>",  clearPointSpace)

updateCanvas()

typeSpace = Frame(base)
typeSpace.grid(row = 1, column = 1, pady = (5, 5))
chooseEu  = Radiobutton(typeSpace, text = "Euclidean", variable = distType, value = 1, command = bindButtons)
chooseEu.pack(anchor = W)
chooseMh  = Radiobutton(typeSpace, text = "Manhattan", variable = distType, value = 2, command = bindButtons)
chooseMh.pack(anchor = W)

labelSpace = Frame(base)
labelSpace.grid(row = 2, column = 0, columnspan = 2, padx = 50)
FName = Entry(labelSpace, bg = 'white', bd = 3)
FName.pack(side = LEFT)
FForm = Entry(labelSpace, bg = 'white', bd = 3)
FForm.pack(side = LEFT)
FForm.bind("<Return>",  updateOutput)
SaveB = Button(labelSpace, bg = '#9999FF', activebackground = '#444499', bd = 3, text = "Save", padx = 3)
SaveB.bind("<Button-1>", updateOutput)
SaveB.pack(side = LEFT)

base.mainloop()