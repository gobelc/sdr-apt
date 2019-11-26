#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019
#	Tallerine Comunicaciones Inalámbricas
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# Authors: Ignacio Bentancur, Ivan Martin, Victoria Martinez
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
import numpy as np
sys.path.insert(0, './extras/')
sys.path.insert(0, './')

import utils
from PIL import Image, ImageDraw


def indice_nubosidad(frame,pos,nivel=180):
    contador=0
    frame2 = frame
    x1=pos[0]
    y1=pos[1]
    x2=pos[2]
    y2=pos[3]
    for q in range(x1,x2):
        for i in range(y1,y2):
            if frame[i,q]<nivel:
                frame2[i,q]=0
            else:
                frame2[i,q]=255
                contador=contador+1

    #utils.plot_image(frame_copy,'Imagen APT')
    index=((1.0*contador)/((x2-x1)*(y2-y1)))*100.0

    return index

