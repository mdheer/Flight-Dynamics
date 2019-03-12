# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:45:24 2019

@author: Mathieu D'heer
"""
from Constants import *


def StationaryValues(hp0, llambda, h, Temp0, g, R, rho0, gamma, p0, Tm, Vc, m, S, c, b, th0, V0): 
    p = hp0 * (1 + ((llambda*h)/Temp0))**(-(g)/(llambda * R))
    rho = rho0 * pow(((1+(llambda * hp0 / Temp0))), (-((g / (llambda*R)) + 1)))
    M = sqrt((2/(gamma -1))* ((1 + (p0/p)*((1 + ((gamma -1)/(2 *gamma)) * (rho0/p0)* Vc**2)**(gamma/(gamma -1)) -1))**((gamma -1)/gamma) -1))
    Temp = Tm/(1 + ((gamma - 1)/2)* M**2)
    W      = m * g
    muc = m / (rho * S * c)
    mub = m / (rho * S * b)
    CX0 = W * sin(th0) / (0.5 * rho * V0 ** 2 * S)
    CZ0 = -W * cos(th0) / (0.5 * rho * V0 ** 2 * S)
    a = sqrt(gamma * R * Temp)
    Vt = M *a
    Ve = Vt * sqrt(rho/rho0)
    return p, rho, M, Temp, W, muc, mub, CX0, CZ0, Vt, Ve




