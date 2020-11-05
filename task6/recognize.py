import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import morphology
from skimage.measure import label, regionprops
from skimage.filters import try_all_threshold, threshold_triangle
from random import choices
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', dest='file', default='symbols.png')
args = parser.parse_args()

def lakes_area(image):
    B = ~image
    BB = np.ones((B.shape[0] + 2, B.shape[1] + 2))
    BB[1:-1, 1:-1] = B
    BB = label(BB)
    BB[BB == 1] = 0
    return label(BB).sum()

def lakes(image):
    B = ~image
    BB = np.ones((B.shape[0] + 2, B.shape[1] + 2))
    BB[1:-1, 1:-1] = B
    return np.max(label(BB)) - 1

def bay_area(image):
    b = ~image
    bb = np.zeros((b.shape[0] + 1, b.shape[1])).astype("uint8")
    bb[:-1, :] = b
    return lakes_area(image)

def vlines(image):
    lines = np.sum(image, 0) // image.shape[0]
    return np.sum(lines)

def has_bay(image):
    b = ~image
    bb = np.zeros((b.shape[0] + 1, b.shape[1])).astype("uint8")
    bb[:-1, :] = b
    return lakes(~bb) - 1

def count_bays(image):
    holes = ~image.copy()
    return np.max(label(holes))

def recognize(region):
    lc = lakes(region.image)
    if lc == 2:
        if vlines(region.image) > 2:
            return "B"
        return "8"
    if lc == 1:
        if has_bay(region.image) > 0:
            return "A"
        if vlines(region.image) > 2:
            bay_relative_area = bay_area(region.image) / region.area
            if bay_relative_area > 0.5:
                return "D"
            return "P"
        return "0"
    if lc == 0:
        if vlines(region.image) > 2:
            if region.extent > 0.95:
                return "-"
            return "1"
        bays = count_bays(region.image)
        if bays == 2:
            return "/"
        if bays > 3:
            circ = region.eccentricity
            if circ < 0.5:
                return "*"
            if bays == 5:
                return "W"
            if bays == 4:
                return "X"
    return None

image = plt.imread(args.file)
image = np.sum(image, 2)
image[image > 0] = 1

labeled = label(image)
print("Number of symbols %i" % np.max(labeled))

regions = regionprops(labeled)
d = {}
for region in regions:
    symbol = recognize(region)
    if symbol not in d:
        d[symbol] = 1
    else:
        d[symbol] += 1

print(d)