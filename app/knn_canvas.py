import math
from copy import deepcopy
from app.utils import multimode

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def dist_deter(k, dist_type, x, y, points):
    distances = []
    for pt in points:
        px, py = pt[0]
        if dist_type == 1:
            distances.append(euclidean_distance(x, y, px, py))
        else:
            distances.append(manhattan_distance(x, y, px, py))

    closest_k = []
    for i in range(2 * k - 1):
        min_val = sorted(distances)[i]
        closest_k.extend([points[j][1] for j, d in enumerate(distances) if d == min_val])
    try:
        return multimode(closest_k)[0]
    except:
        return 0

def canvas_determine(k, dist_type, width, height, points):
    canvas = [[0 for _ in range(width)] for _ in range(height)]
    if dist_type not in [1, 2]:
        return (canvas, 1)

    for y in range(height):
        for x in range(width):
            canvas[y][x] = dist_deter(k, dist_type, x, y, points)

    for pt in points:
        canvas[pt[0][1]][pt[0][0]] = pt[1]
    return (canvas, 0)
