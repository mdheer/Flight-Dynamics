#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: willemvolker
"""
from constants import *

mub = 1 #to be determined
Db = 1 #to be determined

C2 = np.matrix([[CYb+(CYbdot-2*mub)*Db, CL, CYp, CYr-4*mub],\
                 [0, -1/2*Db, 1, 0],\
                 [Clb, 0, Clp-4*mub*Kx2*Db, Clr+4*mub*KXZ*Db],\
                 [Cnb+Cnbdot*Db, 0, Cnp+4*mub*KXZ*Db, Cnr-4*mub*KZ2*Db]])

C3 = np.matrix([[-CYda, -CYdr],\
                [0, 0],\
                [-Clda, -Cldr],\
                [-Cnda, -Cndr]])
