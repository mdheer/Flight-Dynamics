# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:55:35 2019

@author: Mathieu D'heer
"""

from Constants import * 
from StationaryValues import * 
#from ss_sym import * 
#from asymm_SS import * 

#Parameters for this program
datalength = 6
plist = []
rholist = []
Mlist = []
Tlist = []
Wlist = []
muclist = []
mublist =  []
CX0list = []
CZ0list = []
V_TASlist = []
Velist = []

#Pressure                  
Tm = [2,3,4,23,1,4]                      # (given)
hp = [1.,2.,3.,4.,5.,4.]    	         # pressure altitude in the stationary flight condition [m] (given)
alpha = [0.1,0.2,0.3,0.4, 0.5, 0.6]      # angle of attack in the stationary flight condition [rad] (given)
th   =  [3,4,6,986,4,3]                  # pitch angle in the stationary flight condition [rad] (given)
h = [100.,200.,400.,500.,600., 700.]           #added (given)
Vc = [5,3,2,6,4,2]                       #added (given)


# Aircraft mass
m = [2.,5.,3.,2.,5.,6.]       # mass [kg]

#Get Stationary Values
for i in range(datalength): 
    p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve = StationaryValues(hp[i], llambda, h[i], T0, g, R, rho0, gamma, p0, Tm[i], Vc[i], m[i], S, c, b, th[i])
    plist.append(p)
    rholist.append(rho)
    Mlist.append(M)
    Tlist.append(T)
    Wlist.append(W)
    muclist.append(muc)
    mublist.append(mub)
    CX0list.append(CX0)
    CZ0list.append(CZ0)
    V_TASlist.append(V_TAS)
    Velist.append(Ve)
    

    
    
    
    
    