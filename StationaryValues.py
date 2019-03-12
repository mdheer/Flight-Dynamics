# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:45:24 2019

@author: Mathieu D'heer
"""
from Constants import *


def SpeedOfSound(gamma , R, T):
    a = sqrt(gamma * R * T)
    
    return a
    
def Mach(V, a):
    M = V/a
    
    return M

def Rho(hp0): 
    rho = rho0 * pow( ((1+(llambda * hp0 / Temp0))), (-((g / (llambda*R)) + 1)))
    
    return rho





print(Mach(1.4))
