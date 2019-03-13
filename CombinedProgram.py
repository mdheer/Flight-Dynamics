# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:55:35 2019

@author: Mathieu D'heer
"""

from Constants import * 
from StationaryValues import * 
from ss_sym import * 
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
alpha = [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # angle of attack in the stationary flight condition [rad] (given)
th   =  [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # pitch angle in the stationary flight condition [rad] (given)
Vc = [121.92333228, 108.54777684, 99.28777692, 82.3111104, 68.42111052, 59.67555504]  #added (given)
TISA = [246.20300399999996, 244.22281599999997, 242.92281599999995, 240.94262799999996, 239.52281599999998, 238.52281599999998] #Temperature Corrected
# Aircraft mass
m = [4000.,4000.,4000.,4000.,4000.,4000.]       # mass [kg]

hpstat1 = stat_1_conv[0]
Vcstat1 = stat_1_conv[1]
Alpha1 = stat_1_conv[2]
FFLstat1 = stat_1_conv[3]
FFRstat1 = stat_1_conv[4]
Tstat1 = stat_1_conv[6]

hpstat2 = stat_2_conv[0]
Vcstat2 = stat_2_conv[1]
FFLstat2 = stat_2_conv[6]
FFRstat2 = stat_2_conv[7]
Tstat2 = stat_2_conv[9]
i = 0
file = open("matlab.dat", "w") 
#for i in range(5):
file.write(hpstat1[1][1])
    
file.write("Hello World") 
file.write("This is our new text file") 
file.write("and this is another line.") 
file.write("Why? Because we can.") 
 
file.close()

#Get Stationary Values
i =0
for i in range(datalength): 
    p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve, a = StationaryValues(hpstat1[1][i], Tstat1[1][i], Vcstat1[1][i], m[i], th[i])
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

#Get output State system Symmetric
#ss_sym(muclist[0], c, V_TASlist[0], Cmadot, KY2, Cxu, CXa, CZ0, CXq, CZu, CZa, CX0, Czq, Cmu, Cma, Cmq, CXde, CZde, Cmde)

