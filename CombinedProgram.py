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
Tm = 1                 # (given)
hp0    =   1.    	   # pressure altitude in the stationary flight condition [m] (given)
alpha0 =    1.         # angle of attack in the stationary flight condition [rad] (given)
th0    =     1.        # pitch angle in the stationary flight condition [rad] (given)
h = 5000               #added (given)
Vc = 5.                #added (given)


# Aircraft mass
m      =      1.       # mass [kg]

#Get Stationary Values
p, rho, M, Temp, W, muc, mub, CX0, CZ0, V0, Ve = StationaryValues(hp0, llambda, h, Temp0, g, R, rho0, gamma, p0, Tm, Vc, m, S, c, b, th0)
