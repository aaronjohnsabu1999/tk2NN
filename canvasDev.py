import math
from copy    import deepcopy
from general import version

if version() >= 3.8:
    from statistics import multimode
else:
    def multimode(data):
        data.sort()
        counts = dict()
        for i in data:
            counts[i] = counts.get(i, 0) + 1
        return([max(counts, key = counts.get)])

def euDist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def mhDist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def colorInitPoints(canvasSet, pointSet):
    for point in pointSet:
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
    for i in range(2*k-1):
        for index in nthMinIndex(i, distances):
            closestK.append(pointSet[index][1])
    try:
        return multimode(closestK)[0]
    except Exception:
        return 0

def distDeter(k, distType, pointX, pointY, pointSet = []):
    distances = []
    for chosenPoint in pointSet:
        if distType == 1:
            distances.append(euDist(pointX, pointY, chosenPoint[0][0], chosenPoint[0][1]))
        else:
            distances.append(mhDist(pointX, pointY, chosenPoint[0][0], chosenPoint[0][1]))
    
    return minK(k, distances, pointSet)
    
def canvasDetermine(k, distType, canvasWidth, canvasHeight, pointSet = []):
    canvasSet = [[0 for x in range(canvasWidth)] for y in range(canvasHeight)]
    if distType not in [1, 2]:
        return (canvasSet, 1)

    for y in range(0, canvasHeight):
        for x in range(0, canvasWidth):
            canvasSet[y][x] = distDeter(k, distType, x, y, pointSet)

    colorInitPoints(canvasSet, pointSet)
    return (canvasSet, 0)