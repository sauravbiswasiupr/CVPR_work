from cPickle import dump, HIGHEST_PROTOCOL
from numpy import zeros, ones, vstack, hstack, sum, max, int32, amax, amin, mean, newaxis, std, abs
from random import shuffle
from scipy.misc import imread, imresize
from math import isnan
from sklearn.decomposition import PCA

import glob
import os.path
from pbar import Progressbar

IMSIZE = 64
REPAINT_PADDING = True
OVERWRITE = False
dataset = 'sicurambb2.differencechannel.whitenedV3.data'
if (os.path.isfile(dataset) == False) | OVERWRITE:
    pass
else:
    raise IOError('dataset file already exists and OVERWRITE==False')

filelist_nongun = glob.glob('datasetmbb2/nongun/*.png')
filelist_gun = glob.glob('datasetmbb2/gun/*.png')


def histogram_correction(img):
    img = img - amin(img)
    img = img / float(max([1.0, amax(img)])) * 255.0
    return img


def paintblackpaddingwhite(img):
    cols = sum(max(img, 0), 1) == 0
    rows = sum(max(img, 1), 1) == 0
    img[rows, :, :] = 255
    img[:, cols, :] = 255
    return img


def whitening(data):
    # code taken from: 
    # https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/decomposition/tests/test_pca.py
    n_samples, n_features = data.shape
    n_components = n_features
    pca = PCA(n_components=n_components, whiten=True)
    X_whitened = pca.fit_transform(data)
    import numpy
    import pdb; pdb.set_trace
    return X_whitened


def normalize(featurevectors):
    featurevectors = featurevectors - mean(featurevectors, 1)[:, newaxis]
    standard_deviation = std(featurevectors, 1) 
    standard_deviation[standard_deviation < 0.01] = 0.01
    featurevectors = featurevectors / standard_deviation[:, newaxis]
    return featurevectors


def extractpixelsfromfiles(filelist):
    nfiles = len(filelist)
    pbar = Progressbar(nfiles)
    image_data = zeros([nfiles, IMSIZE * IMSIZE])
    for i, fname in enumerate(filelist):
        pbar.update(i)
        img = imread(fname).astype(int32) 
        if REPAINT_PADDING:
            img = paintblackpaddingwhite(img)
        img = imresize(img, (IMSIZE, IMSIZE)).astype(int32) 
        #  as an experiment we use a B-R difference channel
        img = (img[:, :, 2] - img[:, :, 0])
        #img = histogram_correction(img)
        image_data[i] = img.reshape(IMSIZE * IMSIZE)       
    return image_data

n_gun_files = len(filelist_gun)
n_nongun_files = len(filelist_nongun)
assert(n_gun_files > 100)
assert(n_nongun_files > 100)


gun_data = extractpixelsfromfiles(filelist_gun)
nongun_data = extractpixelsfromfiles(filelist_nongun)

data = vstack([gun_data, nongun_data])
data = whitening(data)
norm_factor = amax(abs(data))
data = data / norm_factor
gun_data2 = data[:n_gun_files]
nongun_data2 = data[n_gun_files:n_gun_files + n_nongun_files]

# kind of asserts
if (isnan(amax(gun_data))) or \
    (isnan(amax(nongun_data)) or \
    amax(data) > 1.1 or \
    amin(data) < -1.1):
    import numpy
    import pdb; pdb.set_trace()

nobs = min((n_gun_files, n_nongun_files))
indeces = range(nobs)
shuffle(indeces)

test_set_x = vstack([gun_data[indeces[:200]], nongun_data[indeces[:200]]])
test_set_y = hstack([ones(200), zeros(200)]).astype('int64')

valid_set_x = vstack([gun_data[indeces[200:400]], nongun_data[indeces[200:400]]])
valid_set_y = hstack([ones(200), zeros(200)]).astype('int64')

train_set_x = vstack([gun_data[indeces[400:]], nongun_data[indeces[400:]]])
train_set_y = hstack([ones(nobs - 400), zeros(nobs - 400)]).astype('int64')

result = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),  (test_set_x, test_set_y)]

try:
    with open(dataset, 'wb') as f:
        dump(result, f, HIGHEST_PROTOCOL)
except IOError as e:
    print 'oh damn'
