#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: willemvolker
"""
from Constants import *
import numpy.linalg as la
import control.matlab as c
import matplotlib.pyplot as plt

#Note: do we use V0??

mub = 1 #?
Db = 1 #?

C1 = [[(CYbdot-2*mub)*b/V0, 0, 0, 0],\
                 [0, -1/2*b/V0, 0, 0],\
                 [0, 0, -4*mub*KX2*b**2/(2*V0**2), 4*mub*KXZ*b**2/(2*V0**2)],\
                 [Cnbdot*b/V0, 0, 4*mub*KXZ*b**2/(2*V0**2), -4*mub*KZ2*b**2/(2*V0**2)]]

C2 = [[CYb, CL, CYp*b/(2*V0), (CYr-4*mub)*b/(2*V0)],\
                 [0, 0, b/(2*V0), 0],\
                 [Clb, 0, Clp*b/(2*V0), Clr*b/(2*V0)],\
                 [Cnb, 0, Cnp*b/(2*V0), Cnr*b/(2*V0)]]

C3 = [[CYda, CYdr],\
                [0, 0],\
                [Clda, Cldr],\
                [Cnda, Cndr]]

A = np.dot(-la.inv(C1), C2)
B = np.dot(-la.inv(C1), C3)
C = np.matrix([[1, 1, 1, 1]])
D = np.matrix([[0, 0]])

eig_as = la.eig(A) #eigenvalues of the A matrix (asymmetric)
sys_as = c.ss(A,B,C,D)

#t = np.arange(0,20.01,0.01)
#y,t = c.impulse(sys_as, t)
#
#plt.plot(t,y)