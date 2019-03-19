
""" ========== PROGRAM FOR AERODYNAMIC COEFFICIENTS ========== """

# Importing standard packages
import numpy as np
from math import *
import matplotlib.pyplot as plt

# Importing constants and calculated parameters from parallel programs
from Constants import *
from CombinedProgram import ThrustStat1FD, rholist1, V_TASlist1, Wlist1, Alpha1


""" ========== PART I. Calculating inputs ========== """

# Calculating total thrust:
Thrust = []
elements = int(len(ThrustStat1FD)/2)
for i in range(elements):
    Thrust.append(ThrustStat1FD[i]+ThrustStat1FD[i+1])
    
# Making Alpha1 a "plain" list for compatibility:
Alpha = []
for alpha in Alpha1:
    Alpha.append(alpha[0])
    

print(Thrust)
print()
print(rholist1)
print()
print(V_TASlist1)
print()
print(Wlist1)
print()
print(Alpha)
    
""" ========== PART II. Function for CL,CD and graphs ========== """

def CL_CD(T, rho, V_TAS, W, alpha):
     
    # Creating (empty) tables for parameters of interest
    C_L = []
    C_L2 = [] 
    C_D = []
    x = alpha
    
    # Loops to fill empty CL and CD tables
    for i in range(len(W)):
        C_L_i= (2*W[i])/(rho[i]*V_TAS[i]*V_TAS[i]*S)
        C_L.append(C_L_i)
        C_L2.append(C_L_i*C_L_i)
    
    for j in range(len(T)):
        C_D_j= (2*T[j])/(rho[j]*V_TAS[j]*V_TAS[j]*S)
        C_D.append(C_D_j)
        
    
    # ---------- PLOTTING ----------
    
    # Size of plot labels:
    title_size = 30
    tick_size = 25
    axes_size = 25
        
    # PLOT 1
    plt.subplot(2,2,1)
    plt.title('Lift Curve',fontsize=title_size)
    plt.tick_params(labelsize=tick_size)
    plt.xlabel('alpha [deg]',fontsize=axes_size)
    plt.ylabel('CL [-]',fontsize=axes_size)
    plt.grid()
    # Calculating the trendline
    z = np.polyfit(x, C_L, 1)
    p1 = np.poly1d(z)
    # Plotting
    plt.plot(x,C_L,'bo-',linewidth=3)
    plt.plot(x,p1(x),"r--",linewidth=3)
    
    # PLOT 2
    plt.subplot(2,2,2)
    plt.title('Drag Curve',fontsize=title_size)
    plt.tick_params(labelsize=tick_size)
    plt.xlabel('alpha [deg]',fontsize=axes_size)
    plt.ylabel('CD [-]',fontsize=axes_size)
    plt.grid()
    # Plotting
    plt.plot(x, C_D,'bo-')
    
    # PLOT 3
    plt.subplot(2,2,3)
    plt.title('Lift-Drag Polar',fontsize=title_size)
    plt.tick_params(labelsize=tick_size)
    plt.xlabel('CD [-]',fontsize=axes_size)
    plt.ylabel('CL [-]',fontsize=axes_size)
    plt.grid()
    # Plotting
    plt.plot(C_D, C_L,'bo-',linewidth=3)
    
    # PLOT 4
    plt.subplot(2,2,4)
    plt.title('Lift-Squared-Drag Polar',fontsize=title_size)
    plt.tick_params(labelsize=tick_size)
    plt.xlabel('CD   [-]',fontsize=axes_size)
    plt.ylabel('CL^2 [-]',fontsize=axes_size)
    plt.grid()
    # Calculating the trendline
    w = np.polyfit(C_L2, C_D, 1)
    p2 = np.poly1d(w)
    # Plotting  
    plt.plot(C_D, C_L2,'bo-')
    plt.plot(p2(C_L2),C_L2,"r--",linewidth=3)
    
    # Adjusting plot settings
    plt.subplots_adjust(wspace=0.4,hspace=0.4)
    
    # Printing trendline
    print()
    print('Trendline for lift curve:')
    print ("y = %.6f*x + (%.6f)"%(z[0],z[1]))
    
    # Calculating desired parameters from trendlines
    alpha0 = np.roots(p1)
    CLa = z[0]
    CD0 = w[1]
    e = 1/(pi*A*w[0])
    
    # Reynolds number 
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
