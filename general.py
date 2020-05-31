from colour import Color
from random import random, randint

def colorPicker(pointSet = []):
    choiceSet = {}
    for point in pointSet:
        if not point[1] in choiceSet:
            choiceSet[point[1]] = Color(rgb=(random(), random(), random()))
    return choiceSet

def generatePoints(canvasWidth, canvasHeight, numLabels, numPoints):
    return [((randint(0, canvasWidth-1), randint(0, canvasHeight-1)), randint(0, numLabels-1))  for i in range(numPoints)]