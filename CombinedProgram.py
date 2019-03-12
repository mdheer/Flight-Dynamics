# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:55:35 2019

@author: Mathieu D'heer
"""

from Constants import * 
from StationaryValues import * 
#from ss_sym import * 
#from asymm_SS import * 

p0 = 2
Tm = 1
hp0    =   1.    	   # pressure altitude in the stationary flight condition [m]
V0     =    1.         # true airspeed in the stationary flight condition [m/sec]
alpha0 =    1.         # angle of attack in the stationary flight condition [rad]
th0    =     1.        # pitch angle in the stationary flight condition [rad]
h = 5000 #added
Vc = 5.  #added


# Aircraft mass
m      =      1.       # mass [kg]

#Get Output Constants
p, rho, M, Temp, W, muc, mub, CX0, CZ0, Vt, Ve = StationaryValues(hp0, llambda, h, Temp0, g, R, rho0, gamma, p0, Tm, Vc, m, S, c, b, th0, V0)
