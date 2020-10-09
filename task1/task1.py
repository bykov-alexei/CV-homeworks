from io import StringIO
import numpy as np

def read(filename):
    with open(filename, 'r') as f:
        size = float(f.readline())
        f.readline()
        img = np.loadtxt(StringIO(f.read()))
    return size, img  

filename = input()
size, img = read(filename)
y, x = np.where(img == 1)
if len(x) == 0:
    print('No object on the image')
else:
    width = np.max(x) - np.min(x)
    print(round(size / width, 4))
