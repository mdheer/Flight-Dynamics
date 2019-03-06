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

mub = 1 #?
Db = 1 #?

C1 = [[(CYbdot-2*mub)*b/V0, 0, 0, 0],\
                 [0, -1/2*b/V0, 0, 0],\
                 [0, 0, -4*mub*KX2*b/V0, 4*mub*KXZ*b/V0],\
                 [Cnbdot*b/V0, 0, 4*mub*KXZ*b/V0, -4*mub*KZ2*b/V0]]

C2 = [[CYb+(CYbdot-2*mub)*Db, CL, CYp, CYr-4*mub],\
                 [0, -1/2*Db, 1, 0],\
                 [Clb, 0, Clp-4*mub*KX2*Db, Clr+4*mub*KXZ*Db],\
                 [Cnb+Cnbdot*Db, 0, Cnp+4*mub*KXZ*Db, Cnr-4*mub*KZ2*Db]]

C3 = [[-CYda, -CYdr],\
                [0, 0],\
                [-Clda, -Cldr],\
                [-Cnda, -Cndr]]

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