import sys
from colour import Color
from random import random, randint
import yaml
from pathlib import Path

def load_config(path="config.yaml"):
    with open(Path(path), "r") as f:
        return yaml.safe_load(f)

def version():
    return sys.version_info[0]

def color_picker(points):
    label_colors = {}
    for point in points:
        label = point[1]
        if label not in label_colors:
            label_colors[label] = Color(rgb=(random(), random(), random()))
    return label_colors

def generate_points(width, height, num_labels, num_points):
    return [((randint(0, width - 1), randint(0, height - 1)), randint(0, num_labels - 1)) for _ in range(num_points)]

try:
    from statistics import multimode
except ImportError:
    def multimode(data):
        freq = {}
        for item in data:
            freq[item] = freq.get(item, 0) + 1
        max_count = max(freq.values())
        return [k for k, v in freq.items() if v == max_count]
