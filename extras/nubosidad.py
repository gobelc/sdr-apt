#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, './extras/')
sys.path.insert(0, './')

import apt
import calibrate as cal
import utils

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def indice_nubosidad(frame,x1,y1,x2,y2):
    '''
    Completar código aquí
    '''

    utils.plot_image(matrix[y1:y2,x1:x2],'Imagen APT ')
    index = 0 

    return index



'''
Decodifico y calibro la señal
'''
matrix = apt.decode('wav/am_demod/2019.03.04.19.30.49.wav', cache = True)
matrix = cal.calibrate(matrix, frame_name="A", debug = False, cache = True) 


'''
Visualizamos la imagen APT para identificar el canal infrarrojo
'''

utils.plot_image(matrix,'Imagen APT ')
matrix_channel_A = utils.get_frame(matrix,"A")
matrix_channel_B = utils.get_frame(matrix,"B")



''''
Invocamos la función que calcula el índice de nubosidad
'''
indice = indice_nubosidad(matrix_channel_A,x1=140,y1=612,x2=750,y2=790)


