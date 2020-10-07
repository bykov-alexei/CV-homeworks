from io import StringIO
import numpy as np

filename = 'figure6.txt'
with open(filename, 'r') as f:
    size = float(f.readline())
    f.readline()
    img = np.loadtxt(StringIO(f.read()))
pic_width = img.shape[1]
print(round(size / pic_width, 4))
