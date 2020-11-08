import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from skimage import filters, measure, morphology

parser = argparse.ArgumentParser()
parser.add_argument('--folder', dest='folder', required=True)
args = parser.parse_args()

count = 0

for file in os.listdir(args.folder):
    print("Processing " + file)

    img = plt.imread(os.path.join(args.folder, file))[50:-50, 50:-50]
    gs = 0.2125 * img[:, :, 0] + 0.7154 * img[:, :, 1] + 0.0721 * img[:, :, 2]
    value = filters.threshold_isodata(gs)
    bn = gs < value

    tmp = np.copy(bn)
    for i in range(50):
        tmp = morphology.binary_dilation(tmp)

    lb = measure.label(tmp)
    bboxes = [region.bbox for region in measure.regionprops(lb) if region.eccentricity > 0.95]
    count += len(bboxes)

if count > 1:
    print('Done. Found %i pencils' % count)
elif len(images) == 1:
    print('Done. Found 1 pencil')
else:
    print('Done. No pencils found')
