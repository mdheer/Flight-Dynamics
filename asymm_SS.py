#!/usr/bin/enV_TAS python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: willemV_TASolker
"""
#from Constants import *
from tryreader import *
import numpy as np
import numpy.linalg as la
import control.matlab as control
import matplotlib.pyplot as plt

def Asymm_SS(V_TAS, mub, PrintAssEigenvalues):
    
    C11 = np.matrix([[(CYbdot-2*mub), 0, 0, 0],
           [0, -1/2, 0, 0],
           [0, 0, -4*mub*KX2, 4*mub*KXZ],
           [Cnbdot, 0, 4*mub*KXZ, -4*mub*KZ2]])
    
    C22 = np.matrix([[CYb, CL, CYp, (CYr-4*mub)],
           [0, 0, 1., 0],
           [Clb, 0, Clp, Clr],
           [Cnb, 0, Cnp, Cnr]])
    
    C33 = np.matrix([[CYda, CYdr],
          [0, 0],
          [Clda, Cldr],
          [Cnda, Cndr]])
    
    A = np.dot(-la.inv(C11),C22)
    B = np.dot(-la.inv(C11),C33)
    C = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
    D = np.matrix([[0., 0.],[0., 0.],[0., 0.],[0., 0.]])
    
    sys = control.ss(A,B,C,D)
    eigs = np.linalg.eig(sys.A)
    eigsdim = eigs[0]*(V_TAS/b)
    
    if PrintAssEigenvalues == True: 
        print("ASSYMETRIC EIGENVALUES ")
        print(eigs[0])
        print(eigsdim)
        print(" ")
        print(" ")
    
    realpart = eigs[0].real
    imagpart = eigs[0].imag
    Period=[]
    HalfT = []
    Dampratio = []
    for i in range(len(realpart)):
        P= ((2*pi)/(imagpart[i]))*(b/V_TAS)
        Period.append(P)
        Thalf= (log(1/2)/realpart[i])*(b/V_TAS)
        HalfT.append(Thalf)
        Damp = -realpart[i]/(realpart[i]**2 + imagpart[i]**2)**0.5
        Dampratio.append(Damp)


#plt.plot(t,y)

#V_TAS = V_TAS_TAS = 3.
#mub = 19.
#CL = 5.
#
#
#yb = V_TAS/b * CYb / (2*mub)
#yphi = V_TAS/b * CL / (2*mub)
#yp = V_TAS/b * CYp / (2*mub)
#yr = V_TAS/b * (CYr-4*mub)/(2*mub)
#yda = V_TAS/b * CYda/(2*mub)
#ydr = V_TAS/b * CYdr/(2*mub)
#
#lb = V_TAS/b * (Clb*KZ2+Cnb*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#lphi = 0
#lp = V_TAS/b * (Clp*KZ2+Cnp*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#lr = V_TAS/b * (Clr*KZ2+Cnr*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#lda = V_TAS/b * (Clda*KZ2+Cnda*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#ldr = V_TAS/b * (Cldr*KZ2+Cndr*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#
#nb = V_TAS/b * (Clb*KXZ+Cnb*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#nphi = 0
#n_p = V_TAS/b * (Clp*KXZ+Cnp*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#nr = V_TAS/b * (Clr*KXZ+Cnr*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#nda = V_TAS/b * (Clda*KXZ+Cnda*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#ndr = V_TAS/b * (Cldr*KXZ+Cndr*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#
#dim = b/(2*V_TAS)
#
#Aa = np.matrix([[yb, yphi, yp*dim, yr*dim],\
#                [0, 0, 2*V_TAS/b*dim, 0*dim],\
#                [lb, 0, lp*dim, lr*dim],\
#                [nb, 0, n_p*dim, nr*dim]])
#Ba = np.matrix([[0, ydr],\
#                [0, 0],\
#                [lda, ldr],\
#                [nda, ndr]])
#
#Ca = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
#Da = np.matrix([[0., 0.],[0., 0.],[0., 0.],[0., 0.]])
#
#sys_as = control.ss(Aa,Ba,Ca,Da)
#eigw_as, eigv_as = la.eig(sys_as.A) #eigenV_TASalues & eigenV_TASectors of A-matrix (asymmetric)
#print(eigw_as)