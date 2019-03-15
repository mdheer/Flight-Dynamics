# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:34:37 2019

@author: mathi
"""
from Constants import *
import numpy as np
from math import *
import matplotlib.pyplot as plt
from CombinedProgram import ThrustStat1FD, rholist1, V_TASlist1, Wlist1, Alpha1

# Calculating total thrust:
Thrust = []
elements = int(len(ThrustStat1FD)/2)
for i in range(elements):
    Thrust.append(ThrustStat1FD[i]+ThrustStat1FD[i+1])
    
# Making Alpha1 a "plain" list for compatibility:
Alpha = []
for alpha in Alpha1:
    Alpha.append(alpha[0])

def CL_CD(T, rho, V_TAS, W, alpha):
      
    C_L = []
    C_L2 = [] 
    for i in range(len(W)):
        C_L_i= 2*W[i]/(rho[i]*V_TAS[i]*V_TAS[i]*S)
        C_L.append(C_L_i)
        C_L2.append(C_L_i*C_L_i)
        
    x = alpha
    
    C_D = []
    for j in range(len(T)):
        C_D_j= 2*T[j]/(rho[j]*V_TAS[j]*V_TAS[j]*S)
        C_D.append(C_D_j)
        
    # Size of plot labels:
    title_size = 25
    tick_size = 20
    axes_size = 20
        
    plt.subplot(2,1,1)
    plt.title('Lift Curve',fontsize=title_size)
    plt.tick_params(labelsize=tick_size)
    plt.xlabel('alpha [deg]',fontsize=axes_size)
    plt.ylabel('CL [-]',fontsize=axes_size)
    plt.grid()
    plt.plot(x, C_L)
    # calc the trendline
    z = np.polyfit(x, C_L, 1)
    p1 = np.poly1d(z)
    plt.plot(x,p1(x),"r--")
    
    plt.subplot(2,1,2)
    plt.title('Drag Polar',fontsize=title_size)
    plt.tick_params(labelsize=tick_size)
    plt.xlabel('CD [-]',fontsize=axes_size)
    plt.ylabel('CL^2 [-]',fontsize=axes_size)
    plt.grid()
    plt.plot(C_L2, C_D)
    # calc the trendline
    w = np.polyfit(C_L2, C_D, 1)
    p2 = np.poly1d(w)
    plt.plot(C_L2, p2(C_L2),"r--")
    
    print()
    print ("y = %.6f*x + (%.6f)"%(z[0],z[1]))
    alpha0 = np.roots(p1)
    CLa = (z[0])
    CD0 = np.roots(p2)[0]
    slope = (w[0])
    e = 1/(pi*A*S)
    
    mu=[]
    Re=[]
    
    for i in range(len(T)):
        mu = mu0*(T[i]/T0)**(1.5)*((T0+110.)/(T[i]+110.))
        Re = rho[i]*V_TAS[i]*c/mu   
    
    print()
    print('CD0 = ',CD0,'    [-]')
    print('e   =  ',e,' [-]')
    print('CLa =  ',CLa,'    [-]')
    
    return CD0, e, CLa

CD0,e,CLa = CL_CD(Thrust, rholist1, V_TASlist1, Wlist1, Alpha)
