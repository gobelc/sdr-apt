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

matrix = apt.decode('wav/am_demod/2019.03.04.16.23.59.wav', cache = False)

'''
Calibrate image with Telemetry Frame
'''
cal = cal.calibrate(matrix,frame_name="A", debug=True, cache=False) # La imagen se puede calibrar con cualquiera de los dos Telemetry Frame


utils.plot_image(utils.flip(cal), 'Imagen APT calibrada')
utils.save_image(utils.flip(cal), 'Imagen APT calibrada')

frameA_cal = utils.get_frame(cal, "A")
frameB_cal = utils.get_frame(cal, "B")


utils.plot_image(utils.flip(frameA_cal), 'Frame A calibrado')
utils.save_image(utils.flip(frameA_cal), 'Frame A calibrado')

utils.plot_image(utils.flip(frameB_cal), 'Frame B calibrado')
utils.save_image(utils.flip(frameB_cal), 'Frame B calibrado')
