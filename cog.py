#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:00:40 2019

@author: willemvolker
"""

from Constants import c
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt

lbs = 0.453592 #kg
inch = 0.0254 #m

ZFM = 10823 #pound (zero fuel mass)
ZFM_mom = 3017130.5
ZFM_mom2 = 2991786.5


xcgdat0 = 280.31 #inch (wrt datum line, at t0)
xcg0 = (xcgdat0 - 261.45) * inch #m (wrt forward end of mac, at t0)
xcg0_prcnt = xcg0*100/c #%c

BEM = 9165*lbs #kg (basic empty mass) 
RM = 14223*lbs #kg (ramp mass)

mlst = []
for i in range(3400,99,-100):
    mlst.append(i)
    
momlst = [9696.97, 9410.62, 9124.80, 8839.04, 8554.05, 8269.06, 7984.34, 7699.60, 7415.33, 7131.00, 6846.96, 6562.82, 6278.47, 5994.04, 5709.9, 5425.64, 5141.16, 4856.56, 4572.24, 4287.76, 4003.23, 3718.52, 3434.52, 3150.18, 2866.30, 2581.92, 2298.84, 2014.80, 1732.53, 1448.40, 1165.42, 879.08, 591.18, 298.16]
for i in range(len(momlst)):
    momlst[i] = momlst[i]*100

#plt.plot(mlst,momlst,'ro')
#plt.plot(mlst,f(mlst))
#plt.xlabel('mass [pounds]')
#plt.ylabel('moment [inch-pounds]')
#plt.show()


fmom = interp.interp1d(mlst,momlst) #inch-pounds (moment arm of fl as a function of fl)

#returns xcg [m] wrt forward end of mac, as a function of the fuel load fl [pound]
def cg(fl):
    m = ZFM + fl
    mom = ZFM_mom + fmom(fl)
    xcgdat = mom/m #inch
    xcg = (xcgdat - 261.45) * inch
    xcg_prcnt = xcg*100/c #%c 
    
    mom2 = ZFM_mom2 + fmom(fl)
    xcgdat2 = mom2/m #inch
    xcg2 = (xcgdat2 - 261.45) * inch
    xcg_prcnt2 = xcg2*100/c
    
    return xcg, xcg2





