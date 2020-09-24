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

"""!@package docstring
Documentation for telemetry module.
More details.
"""

#import config

import numpy as np


#NOAA_LINE_LENGTH = config.NOAA_LINE_LENGTH
NOAA_LINE_LENGTH = 2080

class Channel():
    def __init__(self,name, description,wavelength_min,wavelength_max):
        self.name = name
        self.description = description
        self.wavelength_min = wavelength_min
        self.wavelength_max = wavelength_max

    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_wavelength_min(self):
        return self.wavelength_min
    
    def get_wavelength_max(self):
        return self.wavelength_max

def get_vector(telemetry_frame):
    """!@brief Returns a vector with averaged samples of frames.

    @param telemetry_frame Telemetry frame.
    """
    telemetry_vector = np.zeros(telemetry_frame.shape[0])
    for i in range(0,len(telemetry_vector)):
        telemetry_vector[i] = np.mean(telemetry_frame[i,:])
    
    return telemetry_vector

def get_frame(matrix, frame):
    """!@brief Devuelve el cuadro de telemetría de una matriz APT, del canal correspondiente.
    @param matrix Matriz APT
    @param frame Canal APT ('A' o 'B')
    @result telemetry_frame Cuadro de telemetría.
    """
    if frame=="A":
        telemetry_frame = matrix[:,1040-46:1040-1]
    if frame=="B":
        telemetry_frame = matrix[:,NOAA_LINE_LENGTH-46:NOAA_LINE_LENGTH]
    return telemetry_frame

def get_space_time_sync_frame(matrix, frame):
    if frame=="A":
        telemetry_frame = matrix[:,40:40+44]
    if frame=="B":
        telemetry_frame = matrix[:,1040+40:1040+40+44]
    return telemetry_frame


def get_thermistor_temp(telemetry):
    """!@brief Devuelve la temperatura del termistor dado un vector de telemetría.
    @param telemetry Vector de telemetría.
    @result temp Temperatura del termistor (en grados Kelvin).
    """
    d0 = 276.628
    d1 = 0.05098
    d2 = 1.371E-6
    d3 = 0
    d4 = 0

    edge_count = 4 * np.mean(telemetry[9:13])

    temp = d0 + d1*edge_count + d2*edge_count**2 + d3*edge_count**3+ d4*edge_count**4

    return temp

def get_channel(telemetry):
    """!@brief Devuelve el objeto channel de AVHRR/3 según se especifica en la guia de usuario NOOA: \n\n
    Channel 1 --> Visible\n
    Channel 2 --> Near-Infrared\n
    Channel 3A --> Near-Infrared\n
    Channel 3B --> Thermal\n
    Channel 4 --> Thermal\n
    Channel 5 --> Thermal
    @param telemetry Vector de telemetría..
    @result Objeto Channel.
    """

    channel_wedge = telemetry[15]

    d_min = 100
    wedge_min = -1
    ch = Channel("Channel NOT detected", "Channel NOT detected",0,0)
    
    for i in range(1,8):
        distance = abs(channel_wedge - telemetry[i])
        if (distance < d_min and distance < 40):
            d_min = distance
            wedge_min = i

    if wedge_min == 1:
        ch = Channel("Channel 1", "Visible. Daytime cloud/surface",.58,.68)
    if wedge_min == 2:
        ch = Channel("Channel 2", "Near Infrared. Surface water delineation, sea surface temperature, vegetative indexing.",.58,.68)
    if wedge_min == 3:
        ch = Channel("Channel 3A", "Near Infrared. Snow / Ice discrimination.",.58,.68)
    if wedge_min == 6:
        ch = Channel("Channel 3B", "Thermal.Forest fire monitoring, nightime cloud mapping, surface temperature.",.58,.68)
    if wedge_min == 4:
        ch = Channel("Channel 4", "Thermal. Sea surface temperature and night cloud mapping, soil misture.",.58,.68) 
    if wedge_min == 5:
        ch = Channel("Channel 5", "Thermal. Sea surface temperature and night cloud mapping.",.58,.68) 

    return ch

def get_peaks(matrix,frame):
    """!@brief Returns an array with indexes representing the start of each Frame.
    @param matrix Complete APT matrix.
    @param frame The Frame to work with ("A" or "B")
    @result peaks Array with starting indexes for each Frame.
    """
    # minimum distance between peaks
    mindistance = 100
    
    sync_telemetry = np.array([31]*8+[63]*8+[95]*8+[127]*8+[159]*8+[191]*8+[223]*8+[255]*8+[0]*8)
    
    telemetry_frame = get_frame(matrix, frame)
    telemetry_vector = np.zeros(telemetry_frame.shape[0])

    for i in range(0,len(telemetry_vector)):
        telemetry_vector[i] = np.mean(telemetry_frame[i,:])
    
    low = np.min(telemetry_vector)
    high = np.max(telemetry_vector)
    delta = high - low
    
    telemetry_vector = np.round(255 * (telemetry_vector - low) / delta)

    peaks=np.array([0])
    corrs=np.array([0])

    for i in range(0,len(telemetry_vector)-len(sync_telemetry)):

            corr = np.dot(sync_telemetry, telemetry_vector[i : i+len(sync_telemetry)])
            
            # if previous peak is too far, keep it and add this value to the
            # list as a new peak
            if i - peaks[-1] > mindistance:
                peaks = np.append(peaks,i)
                corrs = np.append(corrs,i)

            # else if this value is bigger than the previous maximum, set this
            # one
            elif corr > corrs[-1]:
                peaks[-1] = i
                corrs[-1] = corr

    return corrs, peaks


def get_mayor_frame(matrix, frame):
    telemetry_frame = get_frame(matrix, frame)
    frame_vector = get_vector(telemetry_frame)
    corrs, peaks = get_peaks(matrix,frame)

    index = np.argmin(corrs)
    frame = frame_vector[index:index+128]
    mayor_frame = np.zeros(16)
        
    for j in range(0,16):
        mayor_frame[j] = np.mean(frame[j*8:(j+1)*8])

    return mayor_frame

def compute_CS(matrix, frame):

    space_time_sync_frame =  get_space_time_sync_frame(matrix, frame)
    
    number_rows = space_time_sync_frame.shape[0]

    space_time_sync_frame_vector = np.zeros(number_rows)

    for j in range(0,number_rows):
        space_time_sync_frame_vector[j] = np.mean(space_time_sync_frame[j,:])

    cs = 0
    j = 0

    for i in range(0,number_rows):
        if space_time_sync_frame_vector[i] > 50:
            cs = cs + space_time_sync_frame_vector[i]
            j = j + 1
    cs = 4 * cs / j

    return cs
