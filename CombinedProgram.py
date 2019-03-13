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
alist = []
#From flight test parameters                  
Tm = [268.65, 266.65, 265.34999999999997, 263.34999999999997, 261.95, 260.95]                             # (given)
hp = [3453.384, 3450.3360000000002, 3450.3360000000002, 3447.288, 3450.3360000000002, 3450.3360000000002] # pressure altitude in the stationary flight condition [m] (given)   	         
alpha = [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # angle of attack in the stationary flight condition [rad] (given)
th   =  [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # pitch angle in the stationary flight condition [rad] (given)
Vc = [121.92333228, 108.54777684, 99.28777692, 82.3111104, 68.42111052, 59.67555504]  #added (given)
FFL = [0.086686542128, 0.06992882395500001, 0.064510915072, 0.052667114258000004, 0.049769162995000005, 0.04913917359]      #Fuel flow left engine
FFR = [0.086056552723, 0.07484274131400001, 0.06829085150200001, 0.058337018903000006, 0.05455708247300001, 0.052793112139] #Fuel flow right engine
TISA = [246.20300399999996, 244.22281599999997, 242.92281599999995, 240.94262799999996, 239.52281599999998, 238.52281599999998] #Temperature Corrected
# Aircraft mass
m = [2.,5.,3.,2.,5.,6.]       # mass [kg]

#Get Stationary Values
for i in range(datalength): 
    p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve, a = StationaryValues(hp[i], llambda, T0, g, R, rho0, gamma, p0, Tm[i], Vc[i], m[i], S, c, b, th[i])
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
    alist.append(a)
    
print(Tlist)
    
    
    
    
    