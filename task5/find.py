import numpy as np
import argparse
import matplotlib.pyplot as plt
from skimage import filters, measure, morphology

parser = argparse.ArgumentParser()
parser.add_argument('--file', dest='file', required=True)
args = parser.parse_args()

img = plt.imread(args.file)[50:-50, 50:-50]
gs = 0.2125 * img[:, :, 0] + 0.7154 * img[:, :, 1] + 0.0721 * img[:, :, 2]
value = filters.threshold_isodata(gs)
bn = gs < value

tmp = np.copy(bn)
for i in range(50):
    tmp = morphology.binary_dilation(tmp)

lb = measure.label(tmp)
bboxes = [region.bbox for region in measure.regionprops(lb) if region.eccentricity > 0.95]
images = [img[bbox[0]:bbox[2], bbox[1]:bbox[3]] for bbox in bboxes]

if len(images) > 1:
    fig, ax = plt.subplots(1, len(images))
    for i, image in enumerate(images):
        ax[i].imshow(image)
        ax[i].axis('off')
    print('Done. Found %i pencils. Check result.png file' % len(bboxes))
    fig.savefig('result.png')
elif len(images) == 1:
    plt.imsave('result.png', images[0])
    print('Done. Found 1 pencil. Check result.png file')
else:
    print('Done. No pencils found')
