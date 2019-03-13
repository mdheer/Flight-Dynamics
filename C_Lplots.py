# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:34:37 2019

@author: mathi
"""
from Constants import *
import numpy as np
from math import *
import matplotlib.pyplot as plt

#W = [1,2,3,4,5,6]
#rho = [1,2,3,4,5,6]
#V_TAS = [1,2,3,4,5,6]
#alpha = [1,2,3,4,5,6]
#T=[1,2,3,4,5,6]

def CL_CD(T, rho, V_TAS, W, alpha):
      
    C_L = []
    C_L2 = []
    for i in range(len(W)):
        C_L_i= 2*W[i]/rho[i]*V_TAS[i]*V_TAS[i]*S
        C_L.append(C_L_i)
        C_L2.append(C_L_i*C_L_i)
    x = alpha 
    
    C_D = []
    for j in range(len(T)):
        C_D_j= 2*T[j]/rho[j]*V_TAS[j]*V_TAS[j]*S
        C_D.append(C_D_j)
        
    plt.subplot(2,1,1)
    plt.plot(x, C_L)
    # calc the trendline
    z = np.polyfit(x, C_L, 1)
    p1 = np.poly1d(z)
    plt.plot(x,p1(x),"r--")
    
    plt.subplot(2,1,2)
    plt.plot(C_L2, C_D) 
    w = np.polyfit(C_L2, C_D , 1)
    p2 = np.poly1d(w)
    plt.plot(C_L2, p2(C_L2),"r--")
    
    print ("y=%.6fx+(%.6f)"%(z[0],z[1]))
    alpha0 = np.roots(p1)
    CLa = (z[0])
    CD0 = np.roots(p2)
    slope = (w[0])
    e = 1/(pi*A*S)
    
    mu=[]
    Re=[]
    for i in range(len(T)):
        
        mu = mu0*(T[i]/T0)**(1.5)*((T0+110.)/(T[i]+110.))
        Re = rho[i]*V_TAS[i]*c/mu    
    return CD0, e, CLa
    