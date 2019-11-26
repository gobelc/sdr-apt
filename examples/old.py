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
import satellite as sat
import calibrate as cal
import thermal
import telemetry as tlmtry
import matplotlib.pyplot as plt

from PIL import Image

matrix = apt.decode('wav/am_demod/sample.wav', cache=True)


#
satellite_direction="S-N"
satellite_NOAA="15"



if satellite_direction == "S-N":
    flip_condition = True
else:
    flip_condition = False


if satellite_NOAA == "19":
    satellite = sat.NOAA_19()
elif satellite_NOAA == "18":
    satellite = sat.NOAA_18()
elif satellite_NOAA == "15":
    satellite = sat.NOAA_15()



'''
Normalize image with Telemetry Frame
'''

frame = "A"

display = True
if display==True:
    matrix_norm = cal.calibrate(utils.mean_filter(matrix,2),frame_name="A")
    if flip_condition:
        matrix_norm = utils.flip(matrix_norm)
    img = Image.fromarray(matrix_norm)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.show()
    img.save('_normalized_image.png')


matrix_dif = utils.mean_filter(matrix,2) - matrix_norm
img = Image.fromarray(matrix_dif)
if img.mode != 'RGB':
    img = img.convert('RGB')
img.show()
img.save('_matrix_dif.png')

'''
Display Telemetry Frames (comparing )
'''
frame = "A"
matrix_filtered = utils.mean_filter(matrix,2)
telemetry_norm = tlmtry.get_frame(cal.calibrate(matrix_filtered,frame_name="A"),frame)
telemetry = tlmtry.get_frame(matrix_filtered,frame)

print "telemetry norm:",telemetry_norm
print "telemetry:",telemetry
tel_image= Image.fromarray(telemetry)
tel_image_norm= Image.fromarray(telemetry_norm)


display = True
if display==True:
    plt.figure()
    plt.title('Telemetry Frame')
    plt.imshow(tel_image, cmap='gray')

display = True
if display==True:
    plt.figure()
    plt.title('Normalized Telemetry Frame')
    plt.imshow(tel_image_norm, cmap='gray')

display = True
if display==True:
    plt.figure()
    plt.title('Telemetry Vector')
    plt.plot(tlmtry.get_vector(telemetry), label='Telemetry Vector')
    plt.plot(tlmtry.get_vector(telemetry_norm), label='Normalized Telemetry Vector')
    plt.legend()
    plt.show()

'''
Histogram
'''

display = False
if display==True:
    utils.plot_histogram(matrix,"Raw Histogram")
    utils.plot_histogram(matrix_filtered,"Raw Filtered")


matrix = matrix_filtered

frame_A = utils.get_frame(matrix, "A")
frame_B = utils.get_frame(matrix, "B")


##SPACE AND TIME FRAME SYNC

space_time_sync_frame =  tlmtry.get_space_time_sync_frame(matrix, "B")
space_time_sync_frame= Image.fromarray(space_time_sync_frame)

display = True
if display==True:
    plt.figure()
    plt.title('SPACE AND TIME FRAME SYNC')
    plt.imshow(space_time_sync_frame, cmap='gray')

'''
Get Thermal Image
'''


temp_min = 1000
temp_max = 0
mayor_frame = tlmtry.get_mayor_frame(matrix, "B")
Cs = tlmtry.compute_CS(matrix, "B")
print "Cs:", Cs
print "mayor frame:", mayor_frame
thermal_matrix = thermal.get_temp_3A(frame_B, mayor_frame, satellite, Cs)

imgt = Image.fromarray(thermal_matrix)
imgt =  np.array(imgt)

numrows, numcols = imgt.shape

def format_coord(x, y):
    col = int(x + 0.5)
    row = int(y + 0.5)
    if col >= 0 and col < numcols and row >= 0 and row < numrows:
        z = -150 + imgt[row, col] * 200 / 255
        return 'x=%1.4f, y=%1.4f, z=%1.4f grados Celcius' % (x, y, z)
    else:
        return 'x=%1.4f, y=%1.4f' % (x, y)


fig, ax = plt.subplots()
plt.figure()
ax.set_title("Thermal image")
cax = ax.imshow(imgt, cmap='jet')
ax.format_coord = format_coord
cbar = fig.colorbar(cax)
plt.show()

'''Add curve levels'''
#contours = contour(thermal_matrix, temp_min-273.15, temp_max-273.15)

thermal_matrix = utils.flip(thermal_matrix) # Let's flip the image!
thermal_matrix = utils.sobel_filter(thermal_matrix) # More filtering...

N = thermal_matrix.shape[0]
M = thermal_matrix.shape[1]

extent = (-40, 40, -40, 40)

X = np.arange(0, M, 1)
Y = np.arange(0, N, 1)
Z = np.array(thermal_matrix)#.astype(np.float64)
Z_norm = -150 + Z * 200 / 255


levels = np.arange(-50, 12, 5)
levels2 = np.arange(-50, 12, 30)

cmap = mpl.cm.get_cmap('rainbow')

imgt = Image.fromarray(thermal_matrix)
imgv = Image.fromarray(frame_A)
imgt =  np.array(imgt)
imgv =  np.array(frame_A)

imgv = imgv
imgt = imgt

Z_norm = -150 + Z * 200 / 255

norm = mpl.cm.colors.Normalize(vmax=abs(Z_norm).max(), vmin=-abs(Z_norm).max())

plt.figure()
plt.grid('on')
plt.hold('on')
plt.title("Thermal image with contours")
contours = plt.contourf(X, Y, Z_norm, levels,interpolation='gaussian',  cmap=mpl.cm.get_cmap(cmap, len(levels) - 1), linestyles='solid', linewdith=3)
plt.colorbar()
#contours = plt.contour(X, Y, Z_norm, levels2, extent = extent, interpolation='gaussian', colors = 'k')
#contours = plt.contour(X, Y, Z, levels, cmap=mpl.cm.get_cmap(cmap, len(levels) - 1))#, norm=norm)  
#plt.clabel(contours)
#plt.axis(aspect='image')
#plt.contour(X, Y, Z, levels, cmap=mpl.cm.get_cmap(cmap, len(levels) - 1), norm=norm)    
#plt.contour(Z, levels, colors='k', origin='upper', extent=extent)
plt.imshow(utils.flip(imgv), cmap='gray')
plt.show()



cm_hot = mpl.cm.get_cmap('gray')
imgB = Image.fromarray(frame_B).convert('L')
imgB = 255 - np.array(imgB)
imgB = cm_hot(imgB)
imgB = np.uint8(imgB * 255)
imgB = Image.fromarray(imgB)
if imgB.mode != 'RGB':
    imgB = imgB.convert('RGB')      
imgB.rotate(180).show()
imgB.rotate(180).save('_frameB.png')

cm_gray = mpl.cm.get_cmap('gray')
imgA = Image.fromarray(frame_A).convert('L')
imgA.rotate(180).show()
imgA.rotate(180).save('_frameA_gray.png')   
imgA = np.array(imgA)
imgA = cm_gray(imgA)
imgA = np.uint8(imgA * 255)
imgA = Image.fromarray(imgA)
if imgA.mode != 'RGB':
    imgA = imgA.convert('RGB')      
imgA.rotate(180).show()
imgA.rotate(180).save('_frameA.png')    

print "Frame A dimensions:", frame_A.shape
print "Frame B dimensions:", frame_B.shape

img_composite = Image.blend(imgA,imgB,.4)
if img_composite.mode != 'RGB':
    img_composite = img_composite.convert('RGB')  
img_composite.rotate(180).show()
img_composite.rotate(180).save('_composite.png')    



utils.plot_histogram(frame_A,"Frame A")
utils.plot_histogram(frame_B,"Frame B")


plt.figure(4)
plt.imshow(frame_A, cmap='gray')
plt.imsave('image_frame_A.png',frame_A)
plt.title('Frame A')
plt.show()

plt.figure(5)
plt.imshow(frame_B, cmap='gray')
plt.imsave('image_frame_B.png',frame_B)
plt.title('Frame B')
plt.show()
'''
composite = (0.5*frame_A + 0.5*frame_B)
composite = scipy.signal.convolve2d(composite, kernel, boundary='symm', mode='same')

plt.figure(6)
plt.imshow(composite, cmap='gray')
plt.imsave('image_composite_im.png',composite)
plt.title('Composite (Frame A + Frame B')
plt.show()


width = composite.shape[0]
height = composite.shape[1]
composite = composite.astype(np.uint8)
rgbmatrix = np.zeros((width,height,3), 'uint8')
rgbmatrix[...,0] = false_color.red_color(frame_A)
rgbmatrix[...,1] = false_color.green_color(frame_B) # green_color(composite/3)
rgbmatrix[...,2] = 0*false_color.blue_color(frame_A)
img = Image.fromarray(rgbmatrix, 'RGB')
img.show()
img.save('image_falso_color.png')
'''
