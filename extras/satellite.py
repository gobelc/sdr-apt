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

class NOAA_15():
    def __init__(self) :
        # PRT coeff d0,d1,d2
        d = [[276.60157 , 0.051045 , 1.36328E-06],
            [276.62531 , 0.050909 , 1.47266E-06],
            [276.67413 , 0.050907 , 1.47656E-06],
            [276.59258 , 0.050966 , 1.47656E-06]]

        vc = [925.4075, 839.8979, 2695.9743] # [channel 4, channel5, channel 3B]
        A = [0.337810, 0.304558, 1.621256] # [channel 4, channel5, channel 3B]
        B = [0.998719, 0.999024, 0.998015] # [channel 4, channel5, channel 3B]

        Ns = [-4.50, -3.61, 0.0] # [channel 4, channel5, channel 3B]
        b0 = [4.76, 3.83, 0.0] # [channel 4, channel5, channel 3B]
        b1 = [-0.0932, -0.0659, 0.0] # [channel 4, channel5, channel 3B]
        b2 = [0.0004524, 0.0002811, 0.0] # [channel 4, channel5, channel 3B]    
        self.name = 'NOAA 15'
        self.d = d
        self.vc = vc
        self.A = A
        self.B = B
        self.Ns = Ns
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        
class NOAA_18():
    def __init__(self) :
        # PRT coeff d0,d1,d2
        d = [[276.601 , 0.05090 , 1.657e-06],
            [276.683 , 0.05101 , 1.482e-06],
            [276.565 , 0.05117 , 1.313e-06],
            [276.615 , 0.05103 , 1.484e-06]]

        vc = [928.1460, 833.2532, 2659.7952] # [channel 4, channel5, channel 3B]
        A = [0.436645, 0.253179, 1.698704] # [channel 4, channel5, channel 3B]
        B = [0.998607, 0.999057, 0.996960] # [channel 4, channel5, channel 3B]

        Ns = [-5.53, -2.22, 0.0] # [channel 4, channel5, channel 3B]
        b0 = [5.82, 2.67, 0.0] # [channel 4, channel5, channel 3B]
        b1 = [-0.11069, -0.04360, 0.0] # [channel 4, channel5, channel 3B]
        b2 = [0.00052337, 0.00017715, 0.0] # [channel 4, channel5, channel 3B] 
        self.name = 'NOAA 18'
        self.d = d
        self.vc = vc
        self.A = A
        self.B = B
        self.Ns = Ns
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2

class NOAA_19():
    def __init__(self) : 
        # PRT coeff d0,d1,d2
        d = [[276.6067 , 0.051111 , 1.405783E-06],
            [276.6119 , 0.051090 , 1.496037E-06],
            [276.6311 , 0.051033 , 1.496990E-06],
            [276.6268 , 0.051058 , 1.493110E-06]]

        vc = [928.9, 831.9, 2670.0] # [channel 4, channel5, channel 3B]
        A = [0.53959, 0.36064, 1.67396] # [channel 4, channel5, channel 3B]
        B = [0.998534, 0.998913, 0.997364] # [channel 4, channel5, channel 3B]

        Ns = [-5.49,-3.39, 0.0] # [channel 4, channel5, channel 3B]
        b0 = [5.70, 3.58, 0.0] # [channel 4, channel5, channel 3B]
        b1 = [-0.11187, -0.05991, 0.0] # [channel 4, channel5, channel 3B]
        b2 = [0.00054668, 0.00024985, 0.0] # [channel 4, channel5, channel 3B]   
        self.name = 'NOAA 19'
        self.d = d
        self.vc = vc
        self.A = A
        self.B = B
        self.Ns = Ns
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2