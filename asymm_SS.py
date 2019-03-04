#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: willemvolker
"""
from Constants import *
import numpy as np
import numpy.linalg as la

mub = 1 #?
Db = 1 #?
V = 1 #?

C1 = np.matrix([[(CYbdot-2*mub)*b/V, 0, 0, 0],\
                 [0, -1/2*b/V, 0, 0],\
                 [0, 0, -4*mub*KX2*b/V, 4*mub*KXZ*b/V],\
                 [Cnbdot*b/V, 0, 4*mub*KXZ*b/V, -4*mub*KZ2*b/V]])

C2 = np.matrix([[CYb+(CYbdot-2*mub)*Db, CL, CYp, CYr-4*mub],\
                 [0, -1/2*Db, 1, 0],\
                 [Clb, 0, Clp-4*mub*KX2*Db, Clr+4*mub*KXZ*Db],\
                 [Cnb+Cnbdot*Db, 0, Cnp+4*mub*KXZ*Db, Cnr-4*mub*KZ2*Db]])

C3 = np.matrix([[-CYda, -CYdr],\
                [0, 0],\
                [-Clda, -Cldr],\
                [-Cnda, -Cndr]])

A = np.dot(-la.inv(C1), C2)
B = np.dot(-la.inv(C1), C3)
