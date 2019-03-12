# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:57:28 2019

@author: Simone
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import Cit_par.py

# Reduced equivalent airspeed

def Ve_thilde(Ve, Ws, W):
    Ve_red = Ve * math.sqrt(Ws/W)
    return Ve_red

def de_star(Cmde, Cm0, Cma, CNwa, Cmtc, W, rho, Ve_red, Tc, S):
    de_red = (-1./Cmde)*(Cm0 + (Cma/CNwa)*(W/(0.5 * rho * Ve_red**2 * S)) + Cmtc * Tc)
    return de_red

def Fe_star(W, xcg, rho, Ve_red, dte):
    Fe_red = ((de[i] - de[i-1])/(Se[i] - Se[i-1])) * Se[i] * ce * (Vh/V)**2 *((Chd/Cmd) * ((xcg - xnfree)/c) * (W/S) - )    






















