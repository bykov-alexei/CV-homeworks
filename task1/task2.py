from io import StringIO
import numpy as np

def shift(img, y, x):
    return np.roll(np.roll(img, y, axis=0), x, axis=1)

with open('img1.txt', 'r') as f:
    f.readline()
    f.readline()
    img1 = np.loadtxt(StringIO(f.read()))
    
with open('img2.txt', 'r') as f:
    f.readline()
    f.readline()
    img2 = np.loadtxt(StringIO(f.read()))

for y in range(img1.shape[0]):
    for x in range(img1.shape[1]):
        shifted = shift(img1, y, x)
        if np.all(img2 == shifted):
            print(y, x)
            exit(0)
