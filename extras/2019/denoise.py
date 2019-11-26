#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019
#	Tallerine Comunicaciones Inalámbricas
#   Instituto de Ingenieria Electrica, Facultad de Ingenieria,
#   Universidad de la Republica, Uruguay.
# 
# Authors: Analía Arimón, Bianca Tarino
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

import wave
import matplotlib.pyplot as plt
import numpy as np

def filtro_promedio(m, cantfilas, cantcolumnas):
	C=np.zeros((cantfilas, cantcolumnas))
	CP=[]
	T=np.zeros((2,1))
	f=0
	for i in range (1, cantfilas-1):
		print(f)
		f=f+1
		for j in range (1, cantcolumnas-1):
			if abs(m[i][j]-m[i-1][j])>30 and abs(m[i][j]-m[i+1][j])>30 and abs(m[i][j]-m[i][j-1])>30 and abs(m[i][j]-m[i][j+1])>30:
				CP.append(m[i-1][j-1])
				CP.append(m[i][j-1])
				CP.append(m[i+1][j-1])
				CP.append(m[i-1][j])
				CP.append(m[i+1][j])
				CP.append(m[i-1][j+1]) 
				CP.append(m[i][j+1])
				CP.append(m[i+1][j+1])
				C[i][j]=np.mean(CP)
				CP=[]
			else:
				C[i][j]=m[i][j]

	C=C.astype(np.uint8)	
	return C

def filtro_mediana(m, sensitivity=30, pasadas=1):
	cantfilas,cantcolumnas = m.shape
	C=np.zeros((cantfilas, cantcolumnas))
	CP=[]
	for k in range(pasadas):
		print "Pasada ", k+1, " de ", pasadas
		T=np.zeros((2,1))
		f=0
		for i in range (1, cantfilas-1):
			#print(f)
			f=f+1
			for j in range (1, cantcolumnas-1):
				if abs(m[i][j]-m[i-1][j])>sensitivity and abs(m[i][j]-m[i+1][j])>sensitivity and abs(m[i][j]-m[i][j-1])>sensitivity and abs(m[i][j]-m[i][j+1])>sensitivity:
					CP.append(m[i-1][j-1])
					CP.append(m[i][j-1])
					CP.append(m[i+1][j-1])
					CP.append(m[i-1][j])
					CP.append(m[i+1][j])
					CP.append(m[i-1][j+1]) 
					CP.append(m[i][j+1])
					CP.append(m[i+1][j+1])
					CP.remove(max(CP))
					CP.remove(min(CP))
					CP.remove(max(CP))
					CP.remove(min(CP))
					CP.remove(max(CP))
					CP.remove(min(CP))
					T[0][0]=CP[0]
					T[1][0]=CP[1]
					C[i][j]=(T[0][0]+T[1][0])/2.0

					CP=[]
				else:
					C[i][j]=m[i][j]
		C=C.astype(np.uint8)
		m = C	
	return C

def filtro_mediana_cambiable(m, cantfilas, cantcolumnas, fil, col):
	C=np.zeros((cantfilas, cantcolumnas))
	CP=[]
	f=0
	for i in range (fil/2, cantfilas-(fil/2)-1):
		print(f)
		f=f+1
		for j in range (col/2, cantcolumnas-(col/2)-1):
			if abs(m[i][j]-m[i-1][j])>30 and abs(m[i][j]-m[i+1][j])>30 and abs(m[i][j]-m[i][j-1])>30 and abs(m[i][j]-m[i][j+1])>30:
				for f1 in range (1, (fil/2)+1):
					for c1 in range (1, (col/2)+1):
						CP=np.append(CP,m[i-f1,j-c1])
						CP=np.append(CP,m[i+f1,j+c1])
						CP=np.append(CP,m[i-f1,j+c1])
						CP=np.append(CP,m[i+f1,j-c1])
						if f1==1:
							CP=np.append(CP,m[i-f1,j])
							CP=np.append(CP,m[i+f1,j])
							CP=np.append(CP,m[i,j+c1])
							CP=np.append(CP,m[i,j-c1])
				Cc=np.array(CP)
				Cc=Cc.astype(np.uint8)
				while max(Cc)-min(Cc)>0 and len(Cc)>2:	
					index1=np.argwhere(Cc==max(Cc))
					Cc= np.delete(Cc, index1[0])
					index2=np.argwhere(Cc==min(Cc))
					Cc= np.delete(Cc, index2[0])

				C[i][j]=Cc[0]
				Cc=np.array([])
				CP=[]
			else:
				C[i][j]=m[i][j]

	C=C.astype(np.uint8)	
	return C

