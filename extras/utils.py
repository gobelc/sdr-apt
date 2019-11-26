#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import sys
sys.path.insert(0, './extras/')
sys.path.insert(0, './')

import numpy as np
import time
import scipy.signal
from scipy import ndimage
import matplotlib.pyplot as plt

from PIL import Image

NOAA_LINE_LENGTH = 2080

class Formatter(object):
    def __init__(self, im):
        self.im = im
    def __call__(self, x, y):
        z = self.im.get_array()[int(y), int(x)]
        return 'x={:.01f}, y={:.01f}, z={:.01f}'.format(x, y, z)

def plot_image(image,title, cmap='gray'):
    fig, ax = plt.subplots()
    im = ax.imshow(image, cmap = cmap)
    ax.format_coord = Formatter(im)
    plt.title(title)
    plt.show()

def save_image(image,title):
    img = Image.fromarray(image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save('./images/'+title+'.png')

def plot_histogram(matrix,title="Histograma", save = False):
    hist,bin_edges = np.histogram(matrix,255)
    plt.figure()
    plt.stem(hist)
    plt.title(title)
    plt.xlabel("Nivel")
    plt.ylabel("Frecuencia")
    plt.axis([0,255,0,np.max(hist)])
    if save:
        plt.savefig('./images/'+title+'.png')
    plt.show(block=True)
    
def get_frame(matrix, frame):
    if frame=="A":
        matrix = matrix[:,39+47-1:NOAA_LINE_LENGTH/2-45-3]
    if frame=="B":
        matrix = matrix[:,NOAA_LINE_LENGTH/2+39+47-1:NOAA_LINE_LENGTH-45-3]
    return matrix

def flip(matrix):
    return np.fliplr(np.flipud(matrix))

def gaussian_filter(matrix):
    kernel = np.array([[1./16, 1./8, 1./16],   #3x3 kernel
                [1./8, 1./4, 1./8],
                [1./16, 1./8, 1./16]])
    
    img = Image.fromarray(matrix)
    img_filtered = scipy.signal.convolve2d(img, kernel, boundary='symm', mode='same')
    return img_filtered

def mean_filter(matrix,size):
    kernel = 1./(size**2) * np.ones((size,size))
    filtered = ndimage.convolve(matrix, kernel, mode='constant', cval=0.0)
    return filtered

def equalize_histogram(matrix):
    img_eq = exposure.equalize_hist(matrix,nbins=256, mask=None)
    return util.img_as_ubyte(img_eq, force_copy=False)