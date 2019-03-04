# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:00:04 2019

@author: mathi
"""
from Constants import *
import control.matlab as control
import numpy as np
from math import *

def ss_sym():
    
    C1 = np.matrix([[-2*muc*(c/V0), 0.,0.,0.],
                     [0., (CZadot - 2*muc)*(c/V0), 0., 0.],
                     [0.,0.,-(c/V0), 0.],
                     [0., Cmadot*(c/V0), 0., -2*muc*KY2*(c/V0)**2]])

    C2 = np.matrix([[CXu, CXa, CZ0, CXq*(c/V0)],
                    [CZu, CZa, -CX0, (CZq + 2*muc)*(c/V0)],
                    [0.,0.,0.,1*(c/V0)],
                    [Cmu, Cma, 0., Cmq*(c/V0)]])
    C3 = np.matrix([[CXde],
                    [CZde],
                    [0.],
                    [Cmde]])
    
    Cs = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
    
    Ds =np.matrix([[0.],[0.],[0.],[0.]])
    
    As = np.dot(-np.linalg.inv(C1),C2)
    Bs = np.dot(-np.linalg.inv(C1),C3)
    
    sys1 = control.ss(As,Bs,Cs,Ds)
    
    print(sys1)
    
