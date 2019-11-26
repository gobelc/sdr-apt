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

import numpy as np


def get_sync_peaks(signal, sync):
    """!@brief Devuelve los indices de comienzo del cuadro de sincronización de una señal APT.
    @param signal Señal APT
    @param sync Vector de sincronización (SyncA o SyncB)
    @result peaks Indices de sincronización.
    """
    # list of maximum correlations found: (index, value)
    peaks_corr = [(0, 0)]

    # minimum distance between peaks
    mindistance = 2000

    # need to shift the values down to get meaningful correlation values
    signalshifted = [x-128 for x in signal]
    sync = [x-128 for x in sync]

    for i in range(0,len(signalshifted) - len(sync)):

        corr = np.dot(sync, signalshifted[i : i+len(sync)])

        # if previous peak is too far, keep it and add this value to the
        # list as a new peak
        if i - peaks_corr[-1][0] > mindistance:
            peaks_corr.append((i, corr))

        # else if this value is bigger than the previous maximum, set this
        # one
        elif corr > peaks_corr[-1][1]:
            peaks_corr[-1] = (i, corr)

    peaks = [i[0] for i in peaks_corr] # retrieve peak indexes from peaks_corr
    
    return peaks 