import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology, measure

img = plt.imread('balls_and_rects.png')[::, ::, :3]
gs = img.sum(axis=2)
lb = measure.label(gs)

figures = {
    'rectangle': {},
    'circle': {},
}

regions = measure.regionprops(lb)
for region in regions:
    cx, cy = map(int, region.centroid)
    color = tuple(img[cx, cy])
    figure = 'circle'
    if region.extent == 1:
        figure = 'rectangle'
    if color in figures[figure]:
        figures[figure][color] += 1
    else:
        figures[figure][color] = 1

print("Number of figures", len(regions))
squares = figures['rectangle']
circles = figures['circle']
print("Number of Squares", sum(squares.values()))
print("Number of Circles", sum(circles.values()))
print("Squares:")
for color in squares:
    print("Color: %s" % str(color), "Number: ", squares[color])
print("Circles:")
for color in circles:
    print("Color: %s" % str(color), "Number: ", circles[color])