from io import StringIO
import numpy as np

def read(filename):
    with open(filename, 'r') as f:
        f.readline()
        f.readline()
        img = np.loadtxt(StringIO(f.read()))
    return img    

def shift(img, y, x):
    return np.roll(np.roll(img, y, axis=0), x, axis=1)

img1 = read('img1.txt')
img2 = read('img2.txt')

for y in range(img1.shape[0]):
    for x in range(img1.shape[1]):
        shifted = shift(img1, y, x)
        if np.all(img2 == shifted):
            print(y, x)
            exit(0)
