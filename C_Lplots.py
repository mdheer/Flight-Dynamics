# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:34:37 2019

@author: mathi
"""
import numpy as np
from math import *
import matplotlib.pyplot as plt

W = [1,2,3,4,5,6]
rho = [1,2,3,4,5,6]
V_TAS = [1,2,3,4,5,6]
alpha = [1,2,3,4,5,6]

def CL_alpha():
    
    C_L = []
    for i in range(len(W)):
        C_L_i= 2*W[i]/rho[i]*V_TAS[i]*V_TAS[i]*S
        C_L.append(C_L_i)
    x = alpha 
    
    plt.plot(x, C_L)
    # calc the trendline
    z = np.polyfit(x, C_L, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
    print ("y=%.6fx+(%.6f)"%(z[0],z[1]))
    alpha0 = np.roots(p)
    C_L_alpha = (z[0])
    plt.show()
    return 
    