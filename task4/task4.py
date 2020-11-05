import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology, measure
from skimage.color import rgb2hsv

def find_cluster(clusters, color):
    return min(clusters, key=lambda x: abs(color - x))

def clusterize(colors):
    clusters = [colors[0]]
    for color in colors[1:]:
        d = abs(color - find_cluster(clusters, color))
        if d > 0.05:
            clusters.append(color)
    return clusters

img = plt.imread('balls_and_rects.png')[::, ::, :3]
hsv = rgb2hsv(img)
gs = img.sum(axis=2)
gs[gs > 0] = 1
lb = measure.label(gs)

figures = {
    'rectangle': {},
    'circle': {},
}

regions = measure.regionprops(lb)
clusters = clusterize(np.unique(hsv[:, :, 0]))
for region in regions:
    cx, cy = map(int, region.centroid)
    color = hsv[cx, cy][0]
    figure = 'circle'
    if region.extent == 1:
        figure = 'rectangle'
    cluster = find_cluster(clusters, color)
    if cluster in figures[figure]:
        figures[figure][cluster] += 1
    else:
        figures[figure][cluster] = 1

print("Number of figures", len(regions))
squares = figures['rectangle']
circles = figures['circle']
print("Number of Squares", sum(squares.values()))
print("Number of Circles", sum(circles.values()))
print("Squares:")

for color in squares:
    print("Color: %s" % str(round(color, 2)), "Number: ", squares[color])
print("Circles:")
for color in circles:
    print("Color: %s" % str(round(color, 2)), "Number: ", circles[color])
