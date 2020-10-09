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
sys.path.insert(0, 'extras/')
sys.path.insert(0, 'temp/')

import config
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import math

def reshape(signal):
    '''
    Find sync frames and reshape the 1D signal into a 2D image.

    # This function is partially based on "apt-decoder" by Zac Stewart and Martin Bernardi
    # <https://github.com/zacstewart/apt-decoder>
    '''
    # sync frame to find: seven impulses and some black pixels (some lines
    # have something like 8 black pixels and then white ones)
    syncA = [0, 128, 255, 128]*7 + [0]*7

    # list of maximum correlations found: (index, value)
    peaks = [(0, 0)]

    # minimum distance between peaks
    mindistance = 2000

    # need to shift the values down to get meaningful correlation values
    signalshifted = [x-128 for x in signal]
    syncA = [x-128 for x in syncA]
    for i in range(len(signal)-len(syncA)):
        corr = np.dot(syncA, signalshifted[i : i+len(syncA)])

        # if previous peak is too far, keep it and add this value to the
        # list as a new peak
        if i - peaks[-1][0] > mindistance:
            peaks.append((i, corr))

        # else if this value is bigger than the previous maximum, set this
        # one
        elif corr > peaks[-1][1]:
            peaks[-1] = (i, corr)

    # create image matrix starting each line on the peaks found
    matrix = np.zeros((len(peaks)-2,2080))
    for i in range(len(peaks) - 2):
        matrix[i,:]= signal[peaks[i][0] : peaks[i][0] + 2080]
    return matrix

def reshape_doppler(signal):
    '''
    Find sync frames and reshape the 1D signal into a 2D image, correcting Doppler Effect by resampling the signal
    between peaks. 

    Finds the sync A frame by looking at the maximum values of the cross
    correlation between the signal and a hardcoded sync A frame.

    The expected distance between sync A frames is 2080 samples, but with
    small variations because of Doppler effect.
    '''
    # sync frame to find: seven impulses and some black pixels (some lines
    # have something like 8 black pixels and then white ones)
    pattern = 5*[0] + 5*[128] +5*[255] + 5*[128]

    pattern = pattern.tolist()
    #syncA =  pattern*7 + [0]*7*5
    n_patterns = 7
    syncA = 8*5*[0] + pattern + [0]*15
    offset = (7-n_patterns)*10
    # list of maximum correlations found: (index, value)
    peaks = [(0, 0)]

    # minimum distance between peaks
    mindistance = 2000*5
    matrix = []
    # need to shift the values down to get meaningful correlation values
    signalshifted = [x-128 for x in signal]
    #syncA = [x-128 for x in syncA]

    print('Correcting Doppler Time Spread...')

    i = 0
    while i < (len(signal)-len(syncA)):
        corr = np.dot(syncA, signalshifted[i : i+len(syncA)])
        # if previous peak is too far, keep it and add this value to the
        # list as a new peak
        if i - peaks[-1][0] > mindistance:
            # create image matrix starting each line on the peaks found
            if len(peaks)>2:
                matrix.append(sig.resample(signal[peaks[-1][0]-offset : i-offset],2080))
            peaks.append((i, corr))
            print('Peaks Found: '+ str(len(peaks)) +' of '+str(int(len(signal)/10400)))
        # else if this value is bigger than the previous maximum, set this
        # one
        elif corr > peaks[-1][1]:
            peaks[-1] = (i, corr)

        i += 1


    return np.array(matrix)

def digitize(signal, plow=.5, phigh=99.5):
    '''
    Convert signal to numbers between 0 and 255.
    '''
    data = []

    (low, high) = np.percentile(signal, (plow, phigh))
    delta = high - low
    data = np.round(255 * (signal - low) / delta)
    data[data < 0] = 0
    data[data > 255] = 255

    return data.astype(np.uint8)

def decode(FILENAME, cache = False):
    '''
    Decodes the signal and returns an APT matrix.
    '''

    if cache == False:
        rate, signal = wav.read(FILENAME)
        if rate == 20800:
            truncate = rate * int(len(signal) // rate)
            signal = signal[:truncate]
            matrix = reshape_doppler(digitize(signal))
            np.save('temp/matrix.npy', matrix)
        else:
            truncate = rate * int(len(signal) // rate)
            signal = signal[:truncate]
            matrix = reshape(digitize(signal))
            np.save('temp/matrix.npy', matrix)
    if cache == True:
        matrix = np.load('temp/matrix.npy')

    return matrix

