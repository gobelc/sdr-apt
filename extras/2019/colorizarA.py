#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019
#	Tallerine Comunicaciones Inalámbricas
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# Authors: Luhana Ferreira, Santiago Márquez
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

import math
import sys

sys.path.insert(0, './extras/')
sys.path.insert(0, './')
import numpy as np
import wave
import matplotlib.pyplot as plt
import apt
import calibrate as cal
import utils
from PIL import Image
import sync

def plot_histogram(matrix, title='Histograma', save = True):
	hist,bin_edges = np.histogram(matrix,255)		
	plt.figure()	
	plt.stem(hist)
	plt.title(title)
	plt.xlabel("Nivel")
	plt.ylabel("Frecuencia")
	plt.axis([0,255,0,np.max(hist)])
	if save:
		plt.savefig('./images/Histograma.png')	
		plt.show(block=True)
	#plot_histogram(matrix_channel_B, 'Infrarrojo')
	return


def RGB(matrix_infrared, matrix_visible,a,b):
	n_filas= matrix_infrared.shape[0]
	n_columnas=matrix_infrared.shape[1]
	matriz_RGB=np.zeros((n_filas,n_columnas,3),dtype=np.uint8)
	for i in range (0,n_filas):
		for j in range (0,n_columnas):
	#nubes
			if matrix_infrared[i,j]>a[0] and matrix_infrared[i,j]<b[0]:
				matriz_RGB[i,j,0]=matrix_visible[i,j]
				matriz_RGB[i,j,1]=matrix_visible[i,j]
				matriz_RGB[i,j,2]=matrix_visible[i,j]
	#agua
			if matrix_infrared[i,j]>a[1] and matrix_infrared[i,j]<b[1]:
				matriz_RGB[i,j,0]=0
				matriz_RGB[i,j,1]=0
				matriz_RGB[i,j,2]=200#matrix_visible[i,j]		
	#tierra
			if matrix_infrared[i,j]>a[2] and matrix_infrared[i,j]<b[2]:
				matriz_RGB[i,j,0]=0#40#matrix_visible[i,j]-210
				matriz_RGB[i,j,1]=101
				matriz_RGB[i,j,2]=0#37	
	'''
			if matrix_infrared[i,j]>a[3] and matrix_infrared[i,j]<b[3]:
				if matrix_visible[i,j]> 34 and matrix_visible[i,j]<80 : #estierra
					matriz_RGB[i,j,0]=matrix_visible[i,j]-210
					matriz_RGB[i,j,1]=101
					matriz_RGB[i,j,2]=37
				else:
					matriz_RGB[i,j,0]=0
					matriz_RGB[i,j,1]=0
					matriz_RGB[i,j,2]=matrix_visible[i,j]	

			if matrix_infrared[i,j]>a[4] and matrix_infrared[i,j]<b[4]:
				if matrix_visible[i,j]>81 : #esnube
					matriz_RGB[i,j,0]=matrix_visible[i,j]
					matriz_RGB[i,j,1]=matrix_visible[i,j]
					matriz_RGB[i,j,2]=matrix_visible[i,j]
				else:
					matriz_RGB[i,j,0]=0
					matriz_RGB[i,j,1]=0
					matriz_RGB[i,j,2]=matrix_visible[i,j]
		'''
	return matriz_RGB


def colorizar(matrix_infrared,matrix_visible,a,b):

	#utils.plot_image(matrix,'Imagen APT ')


	#utils.plot_image(matrix_channel_B, 'titulo')
	'''plt.imshow(matrix_channel_A)
	plt.show()
	plt.imshow(matrix_channel_B)
	plt.show()'''

	array=RGB(matrix_infrared,matrix_visible,a,b)
	img=Image.fromarray(array.astype('uint8'),'RGB')
	img.show()
				
	return