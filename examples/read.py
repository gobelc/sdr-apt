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
import calibrate as cal

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

from PIL import Image


date = '2019.03.04.19.30.49'
calibrar = True

matrix = apt.decode('wav/am_demod/'+date+'.wav', cache = False)

if calibrar:
    matrix = cal.calibrate(matrix, frame_name="A", debug = False, cache = False) 

utils.plot_image(matrix,'Imagen APT ' + date)
utils.save_image(matrix,'Imagen APT ' + date)

frameA = utils.get_frame(matrix,"A")
frameB = utils.get_frame(matrix,"B")

utils.plot_image(frameA,'Imagen Canal A ' + date)
utils.save_image(frameA,'Imagen Canal A ' + date)

utils.plot_image(frameB,'Imagen Canal B ' + date)
utils.save_image(frameB,'Imagen Canal B ' + date)


