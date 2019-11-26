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

import apt
import utils
import numpy as np
import scipy.signal

from PIL import Image

matrix = apt.decode('wav/am_demod/sample.wav')

'''
Blur Filter
'''
kernel = (1/8.) *  np.array(   [[ 1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]])

img = Image.fromarray(matrix)
img_filtered = scipy.signal.convolve2d(img, kernel)
img_filtered.astype(np.uint8)

img = Image.fromarray(img_filtered)
if img.mode != 'RGB':
    img = img.convert('RGB')
img.show()
img.save('./images/blur_filter.png')



'''
Sobel Filter Sx
'''
kernel = (1/2.) *  np.array(   [[ -1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])

img = Image.fromarray(matrix)
img_filtered = scipy.signal.convolve2d(img, kernel)
img_filtered.astype(np.uint8)


img = Image.fromarray(img_filtered)
if img.mode != 'RGB':
    img = img.convert('RGB')
img.show()
img.save('./images/sobel_filter_sx.png')

'''
Sobel Filter Sy
'''
kernel = (1/8.) *  np.array(   [[1, 2, 1],
                                [0, 0, 0],
                                [-1, -2, -1]])

img = Image.fromarray(matrix)
img_filtered = scipy.signal.convolve2d(img, kernel)
img_filtered.astype(np.uint8)

img_filtered[img_filtered >= 100 ] = 255
img_filtered[img_filtered < 100 ] = 0


img = Image.fromarray(img_filtered)
if img.mode != 'RGB':
    img = img.convert('RGB')
img.show()
img.save('./images/sobel_filter_sy.png')

'''
Sobel Filter Sxy
'''
kernel = (1/2.) *  np.array(   [[ -1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])

img = Image.fromarray(matrix)
img_filtered = scipy.signal.convolve2d(img, kernel)
img_filtered.astype(np.uint8)


img = Image.fromarray(img_filtered)
if img.mode != 'RGB':
    img = img.convert('RGB')
img.show()
img.save('./images/sobel_filter_sxy.png')

