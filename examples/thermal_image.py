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



satellite_NOAA="15"


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
matrix_norm = cal.calibrate(utils.mean_filter(matrix,2),frame_name="A")

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

frame_A = utils.get_frame(matrix_filtered, "A")
frame_B = utils.get_frame(matrix_filtered, "B")


##SPACE AND TIME FRAME SYNC
space_time_sync_frame =  tlmtry.get_space_time_sync_frame(matrix, "B")
space_time_sync_frame= Image.fromarray(space_time_sync_frame)


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
        z = -150.0 + imgt[row, col] * 200 / 255.0
        return 'x=%1.4f, y=%1.4f, Temperatura = %1.4f grados Celcius' % (x, y, z)
    else:
        return 'x=%1.4f, y=%1.4f' % (x, y)


fig, ax = plt.subplots()
plt.figure()
ax.set_title("Thermal image")
cax = ax.imshow(imgt, cmap='jet')
ax.format_coord = format_coord
cbar = fig.colorbar(cax)
plt.show()
