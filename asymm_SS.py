#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: willemvolker
"""
from Constants import *
import numpy as np
import numpy.linalg as la
import control.matlab as c
import matplotlib.pyplot as plt


##test values from reader
#V0 = 59.9
#S = 24.2
#b = 13.36
#CL = 1.136
#mub = 15.5
#KX2 = 0.012
#KZ2 = 0.037
#KXZ = 0.002
#CYb = -0.9896
#CYp = -0.0870
#CYr = 0.4300
#CYda = 0
#CYdr = 0.3037
#Clb = -0.0772
#Clp = -0.3444
#Clr = 0.2800
#Clda = -0.2349
#Cldr = 0.0286
#Cnb = 0.1638
#Cnp = -0.0108
#Cnr = -0.1930
#Cnda = 0.0286
#Cndr = -0.1261
#CYbdot = 0 #neglect (see chapter 11)
#Cnbdot = 0 #neglect (see chapter 11)

#Note: do we use V0??



#C1 = np.matrix([[(CYbdot-2*mub)*b/V0, 0, 0, 0],\
#       [0, -1/2*b/V0, 0, 0],\
#       [0, 0, -4*mub*KX2*b**2/(2*V0**2), 4*mub*KXZ*b**2/(2*V0**2)],\
#       [Cnbdot*b/V0, 0, 4*mub*KXZ*b**2/(2*V0**2), -4*mub*KZ2*b**2/(2*V0**2)]])
#
#C2 = np.matrix([[CYb, CL, CYp*b/(2*V0), (CYr-4*mub)*b/(2*V0)],\
#       [0, 0, b/(2*V0), 0],\
#       [Clb, 0, Clp*b/(2*V0), Clr*b/(2*V0)],\
#       [Cnb, 0, Cnp*b/(2*V0), Cnr*b/(2*V0)]])
#
#C3 = np.matrix([[CYda, CYdr],\
#      [0, 0],\
#      [Clda, Cldr],\
#      [Cnda, Cndr]])
#
#Aa = la.inv(-C1)* C2
#Ba = la.inv(-C1)*C3


#t = np.arange(2,20.01,0.01)
#y,t = c.step(sys_as, t)

#plt.plot(t,y)

V = V_TAS = 3.
mub = 19.
CL = 5.

def assym_SS (V, b, CYb, mub, CL, CYp, CYr, CYda, CYdr, Clb, KZ2, Cnb, KXZ, KX2, Cnp):
    
    yb = V/b * CYb / (2*mub)
    yphi = V/b * CL / (2*mub)
    yp = V/b * CYp / (2*mub)
    yr = V/b * (CYr-4*mub)/(2*mub)
    yda = V/b * CYda/(2*mub)
    ydr = V/b * CYdr/(2*mub)
    
    lb = V/b * (Clb*KZ2+Cnb*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
    lphi = 0
    lp = V/b * (Clp*KZ2+Cnp*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
    lr = V/b * (Clr*KZ2+Cnr*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
    lda = V/b * (Clda*KZ2+Cnda*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
    ldr = V/b * (Cldr*KZ2+Cndr*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
    
    nb = V/b * (Clb*KXZ+Cnb*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
    nphi = 0
    n_p = V/b * (Clp*KXZ+Cnp*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
    nr = V/b * (Clr*KXZ+Cnr*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
    nda = V/b * (Clda*KXZ+Cnda*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
    ndr = V/b * (Cldr*KXZ+Cndr*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
    
    dim = b/(2*V)
    
    Aa = np.matrix([[yb, yphi, yp*dim, yr*dim],\
                    [0, 0, 2*V/b*dim, 0*dim],\
                    [lb, 0, lp*dim, lr*dim],\
                    [nb, 0, n_p*dim, nr*dim]])
    Ba = np.matrix([[0, ydr],\
                    [0, 0],\
                    [lda, ldr],\
                    [nda, ndr]])
    
    Ca = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
    Da = np.matrix([[0., 0.],[0., 0.],[0., 0.],[0., 0.]])
    
    eigw_as, eigv_as = la.eig(Aa) #eigenvalues & eigenvectors of A-matrix (asymmetric)
    sys_as = c.ss(Aa,Ba,Ca,Da)