import numpy as np
import matplotlib.pyplot as plt
import skimage.morphology as m
from skimage.measure import label
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', dest='img')
args = parser.parse_args()

def count(img, masks):
    img = np.copy(img)
    n = []
    for mask in masks:
        opened = m.binary_opening(img, mask)
        lb = label(opened)
        img = img - opened
        n.append(lb.max())
    return n

img = np.load(args.img)
masks = [
    np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]),
    np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1]]),
    np.array([[1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]),
    np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]),
]

counts = count(img, masks)

fig, ax = plt.subplots(len(masks))
fig.suptitle("Total: " + str(sum(counts)))
fig.set_figheight(10)
fig.set_figwidth(6)
for i, (mask, count) in enumerate(zip(masks, counts)):
    ax[i].axis('off')
    ax[i].imshow(mask, vmin=0, vmax=1)
    ax[i].set_title(count)
print('Check result.png file')
fig.savefig('result.png')