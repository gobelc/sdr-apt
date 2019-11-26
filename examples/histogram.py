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


utils.plot_histogram(matrix,'Imagen completa')
utils.plot_image(matrix,'Imagen completa')

# Giro la imagen 180 grados porque el satélite recorría de Sur a Norte
frameA = utils.flip(utils.get_frame(matrix,"A"))
frameB = utils.flip(utils.get_frame(matrix,"B"))

#
utils.plot_histogram(frameB,'Histograma Banda Infrarroja', save = True)
utils.plot_histogram(frameA,'Histograma Espectro visible', save = True)
