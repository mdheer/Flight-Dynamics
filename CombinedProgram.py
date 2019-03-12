# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:55:35 2019

@author: Mathieu D'heer
"""

from Constants import * 
from StationaryValues import * 
#from ss_sym import * 
#from asymm_SS import * 

#Variables Program
datalength = 6
                 
#Input parameters
Tm     = [1,2,3,4,5,6]                 # (given)
hp0    = [0.1,0.2,0.3, 0.4, 0.5, 0.6]   	   # pressure altitude in the stationary flight condition [m] (given)
alpha0 = [3,2,5,1,5,6]        # angle of attack in the stationary flight condition [rad] (given)
th0    = [6,7,8,9,7,3]       # pitch angle in the stationary flight condition [rad] (given)
h      = [1000,2000,3000,4000,6000,3000]             #added (given)
Vc     = [5303, 5893, 68493, 69894, 8392,7583]                 #added (given)


# Aircraft mass
m      =      1.       # mass [kg]

#Get Stationary Values
for i in range(datalength): 
    
    p, rho, M, Temp, W, muc, mub, CX0, CZ0, V0, Ve = StationaryValues(hp0, llambda, h, Temp0, g, R, rho0, gamma, p0, Tm, Vc, m, S, c, b, th0)
