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

#import config
import telemetry as tltry
import numpy as np
import scipy
import matplotlib.pyplot as plt


#NOAA_LINE_LENGTH = config.NOAA_LINE_LENGTH
NOAA_LINE_LENGTH = 2080

def calibrate(matrix,frame_name, debug = False, cache = False):
    """!@brief Devuelve la matriz calibrada a partir de un Frame completo de Telemetría.
    @param matrix Matriz APT
    @param frame El Frame con el que trabajar ("A" o "B")
    @result matrix Matriz calibrada.
    """
    if cache==False:
        print "\n Normalizando imagen... \n"
        TELEMETRY_LENGTH = 8 * 16

        _, peaks =  tltry.get_peaks(matrix,frame_name)
        telemetry_frame = tltry.get_frame(matrix,frame_name)

        r_max = 0
        for i in range(0,len(peaks)):
            peak = peaks[i]
            print "\n ############### \n Normalizando frame", i+1, "de", len(peaks), "frames."

            telemetry_vector = tltry.get_vector(telemetry_frame[peak:peak+TELEMETRY_LENGTH])
            telemetry = np.zeros(16)
            
            for j in range(0,16):
                telemetry[j] = np.mean(telemetry_vector[j*8:(j+1)*8])

            print "\n Telemetria recibida: ", telemetry

            ch = tltry.get_channel(telemetry)
            if i==0:
                channel = ch

            p = polynome(telemetry)
            r = rsquared(np.append(p(telemetry[8]),p(telemetry[0:8])), [0,31,63,95,127,159,191,223,255])

            print "\n Polinomio de ajuste:", p, "| r =", r
            
            if r > r_max:
                r_max = r
                channel = ch
                p_max = p

            if r>0.99:
                print "\n Canal del frame", frame_name, ": ", channel.get_name()
                print "\n Descripción del canal:", channel.get_description(),
                print "\n Temperatura de termistor:", tltry.get_thermistor_temp(telemetry)

            if i == len(peaks)-1:
                lower_index = peak
                upper_index = matrix.shape[0]
            elif i == 0 :
                lower_index = 0
                upper_index = peak
            else:
                upper_index = peaks[i+1]
                lower_index = peak
            
       
            if debug:
                print "\n Telemetria calibrada:", p(telemetry[0:16])

                plt.figure()
                
                plt.title('Calibracion de imagen (Frame %d)' %(i+1))
                plt.plot(np.append(telemetry[8],telemetry[0:8]), label = "detectado",marker='o')
                plt.plot(np.append(p(telemetry[8]),p(telemetry[0:8])), label = "calibrado",marker='o')
                plt.plot(np.array([0,31,63,95,127,159,191,223,255]), label = "esperado",marker='v')
                plt.legend()
                plt.show()

        for j in range(0,NOAA_LINE_LENGTH):
            for k in range(0,matrix.shape[0]):
                new_pixel = p_max(matrix[k,j])
                #print "New:", new_pixel, "Old:", matrix[k,j]
                if new_pixel<0:
                    matrix[k,j] = 0
                elif new_pixel>255:
                    matrix[k,j] = 255
                else:
                    matrix[k,j] = new_pixel
        np.save('temp/matrix_calibrated'+frame_name+'.npy', matrix)
    
    if cache==True:
        matrix = np.load('temp/matrix_calibrated'+frame_name+'.npy')

    return matrix




def polynome(telemetry):
    """!@brief Returns a first order approximation to normalize samples from telemetry data.
    @param telemetry Averaged telemetry data.
    @result p The polynome.
    """    
    Y = np.append(telemetry[8],telemetry[0:8])
    X = np.array([0,31,63,95,127,159,191,223,255])

    z = np.polyfit(Y,X,1)

    p = np.poly1d(z)
    return p

def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2