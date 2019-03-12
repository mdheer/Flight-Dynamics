# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:45:24 2019

@author: Mathieu D'heer
"""
from Constants import *


def StationaryValues(hp, llambda, T0, g, R, rho0, gamma, p0, Tm, Vc, m, S, c, b, th): 
    p = p0 * (1 + ((llambda*hp)/T0))**(-(g)/(llambda * R))
    rho = rho0 * pow(((1+(llambda * hp / T0))), (-((g / (llambda*R)) + 1)))
    M = sqrt((2/(gamma -1))* ((1 + (p0/p)*((1 + ((gamma -1)/(2 *gamma)) * (rho0/p0)* Vc**2)**(gamma/(gamma -1)) -1))**((gamma -1)/gamma) -1))
    T = Tm/(1 + ((gamma - 1)/2)* M**2)
    W = m * g
    muc = m / (rho * S * c)
    mub = m / (rho * S * b)
    a = sqrt(gamma * R * T)
    V_TAS = M *a
    Ve = V_TAS * sqrt(rho/rho0)
    CX0 = W * sin(th) / (0.5 * rho * V_TAS ** 2 * S)
    CZ0 = -W * cos(th) / (0.5 * rho * V_TAS ** 2 * S)
    return p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve, a




