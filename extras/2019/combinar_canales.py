#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019
#	Tallerine Comunicaciones Inalámbricas
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# Authors: Agustina Armanderiz, Damián Castro, Emilia Fender
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
import matplotlib.pyplot as plt
from PIL import Image
import sync
import scipy.signal as signal
from scipy import ndimage


def saturar(matriz):
	matriz_saturada = matriz
	for i in range(0, matriz.shape[0]):
		for j in range(0, matriz.shape[1]):
			if matriz[i,j] < 0:
				matriz_saturada[i,j] = 0
			elif matriz[i,j] > 255:
				matriz_saturada[i,j] = 255
	return matriz_saturada

def superposicion (matriz,n1,n2):
	alto = len (matriz)
	ancho = 2080
	z=matriz[0:(alto+1),0:1040].astype(np.float64)
	y=matriz[0:(alto+1),1040:2080].astype(np.float64)
	cl=n1*z+n2*y
	suma_ponderada=cl#/1.*(n1+n2)
	matrix = saturar(suma_ponderada)
	final=matrix.astype("uint8")
	return final

def combinar(matrix,c1=1.,c2=-.5):	
	a=superposicion(matrix,c1,c2)
	img=Image.fromarray(a, mode=None)
	if img.mode!='RGB':
		img=img.convert('RGB')
		img.save('./images/kernelident.png')
	return a
