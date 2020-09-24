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

import math
import satellite as sat
import numpy as np
import calibrate as cal
import telemetry as tlmtry
import utils

from PIL import Image
import matplotlib.pyplot as plt


def getThermalImage(matrix, satellite_NOAA="19",frame_name="A"):
        temp_min = 1000
        temp_max = 0
        if satellite_NOAA == "19":
                satellite = sat.NOAA_19()
        elif satellite_NOAA == "18":
                satellite = sat.NOAA_18()
        elif satellite_NOAA == "15":
                satellite = sat.NOAA_15()
        matrix = cal.calibrate(utils.mean_filter(matrix,2),frame_name)
        #matrix = utils.mean_filter(matrix,2)
        frame = utils.get_frame(matrix, frame_name)
        mayor_frame = tlmtry.get_mayor_frame(matrix, frame_name)
        Cs = tlmtry.compute_CS(matrix, frame_name)
        print("Cs:", Cs)
        print("mayor frame:", mayor_frame)
        thermal_matrix = get_temp_3A(frame, mayor_frame, satellite, Cs)
        imgt = Image.fromarray(thermal_matrix)
        imgt =  np.array(imgt)
        numrows, numcols = imgt.shape
        return thermal_matrix


def get_temp_3A(matrix, telemetry, satellite, Cs):


    satelite = satellite

    c1=1.1910427e-5
    c2=1.4387752
    
    print("largo telemetria: ", len(telemetry))
   
    Ns = satelite.Ns[2]
    b0 = satelite.b0[2]
    b1 = satelite.b1[2]
    b2 = satelite.b2[2]

    print("Ns", Ns)
    print("bo", b0)
    print("b1", b1)
    d = np.matrix(satelite.d)
    d0 = d[:,0]
    d1 = d[:,1]
    d2 = d[:,2]

    CPRO = 4 * telemetry[9]
    CPR1 = 4 * telemetry[10]
    CPR2 = 4 * telemetry[11]
    CPR3 = 4 * telemetry[12]

    print(CPRO)
    T0 = d0[0] + d1[0] * CPRO + d2[0] * CPRO**2 
    T1 = d0[1] + d1[1] * CPR1 + d2[1] * CPR1**2 
    T2 = d0[2] + d1[2] * CPR2 + d2[2] * CPR2**2 
    T3 = d0[3] + d1[3] * CPR3 + d2[3] * CPR3**2 
  
    print(T0)

    Tbb = .25 * (T0 + T1 + T2 + T3)
    Tbb = satelite.A[2] + Tbb * satelite.B[2]
    Tbb = Tbb[0,0]
    vc =  satelite.vc[2]

    print("vc", vc)
    print("Tbb", Tbb)
    Nbb = c1 * vc**3 / (math.exp(c2 * vc / Tbb) - 1.0)

    Cb = telemetry[14] * 4

    print("Cb", Cb)
    print("Cs", Cs)

    matrix_therm = np.ndarray(( matrix.shape[0],  matrix.shape[1]))
    for i in range(0, matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            Ce = np.array(matrix[i,j]).astype(np.float64)
            N1 = Ns + (Nbb-Ns) * (Cs-Ce*4) / (Cs-Cb)
            Nc = b0 + b1*N1 + b2*N1**2
            Ne = N1 + Nc
            T = c2*vc / math.log(abs(c1*(vc**3)/Ne+1.0))
            T = (T - satelite.A[2]) / (satelite.B[2]) 
            T = (T - 273.15 + 150) / 200.0 * 256.0 #  range 0-255 for -150 +50 celcius
            matrix_therm[i,j] = T

    return matrix_therm