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
import calibrate as cal
import utils
import numpy as np
import scipy.signal

from PIL import Image

matrix = apt.decode('wav/am_demod/sample.wav', cache = True)



'''
Calibrate image with Telemetry Frame
'''
matrix_norm = cal.calibrate(matrix, frame_name="A", cache=True) 



'''
Blur Filter
'''
kernel_gauss_9 = (1/16.) *  np.array(   [[ 1, 2, 1],
                                [2,4,2],
                                [1,2,1]])

kernel_gauss_256 = (1/256.) *  np.array(   [[ 1, 4, 6,4,1],
                                [4,16,24,16,4],
                                [6,24,36,24,6],
                                [4,16,24,16,4],
                                [1,4,6,4,1]])

img = Image.fromarray(matrix_norm)
matrix_filtered = scipy.signal.convolve2d(img, kernel_gauss_9)
matrix_filtered.astype(np.uint8)



img = Image.fromarray(matrix_filtered)
#img.show()
#img.save('./images/calibrated_image_B.png')



frameA = utils.flip(utils.get_frame(matrix_filtered,"A"))
frameB = utils.flip(utils.get_frame(matrix_filtered,"B"))

'''
img = Image.fromarray(frameA)
img.show()

img = Image.fromarray(frameB)
img.show()


composite = frameA/2 + frameB/2
img = Image.fromarray(composite)
img.show()
'''

width = frameB.shape[0]
height = frameB.shape[1]
rgbmatrix = np.ones((width,height,3), 'uint8')

utils.plot_histogram(frameB,'Infrarojo')
utils.plot_histogram(frameA,'Visible')
utils.plot_image(frameA,"Visible")
utils.plot_image(frameB,"Infrarojo")

ocean = False
land = False
cloud=False
for i in range(0, width):
    for j in range(0, height):
        ocean = False
        land = False
        cloud= False
        pixel = frameA[i,j]
        if frameA[i,j]<40:
            ocean == True
        if (frameB[i,j] >=100 and frameB[i,j] <= 140) and (frameA[i,j]<60) and ocean == False: #oceano
            rgbmatrix[i,j,...] =  [0,pixel,3*pixel]
            ocean = True
        if (frameB[i,j] < 110 or frameA[i,j]<46) and frameA[i,j]<110 and ocean == False:   #tierra                   
            rgbmatrix[i,j,...] =  [pixel/2,pixel,0]
            land = True
        if frameB[i,j] > 100 and ocean==False and land ==False:  #nubes
            rgbmatrix[i,j,...] =  [pixel+50,pixel+50,pixel+50]


img = Image.fromarray(rgbmatrix, 'RGB')
#img.show()
img.save('./images/image_falso_color.png')

#utils.plot_histogram(frameB)
