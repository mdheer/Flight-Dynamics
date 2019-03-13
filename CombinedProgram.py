# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:55:35 2019

@author: Mathieu D'heer
"""

from Constants import * 
from StationaryValues import * 
from ss_sym import * 
#from asymm_SS import * 
"""################################################Parameters used################################################"""
datalength = 6
numberdatasets = 2
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
TISA = []
hplist = []
#From flight test parameters                  

th   =  [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # pitch angle in the stationary flight condition [rad] (given)
TISA = [246.20300399999996, 244.22281599999997, 242.92281599999995, 240.94262799999996, 239.52281599999998, 238.52281599999998] #Temperature Corrected
# Aircraft mass
m = [4000.,4000.,4000.,4000.,4000.,4000.]       # mass [kg]


"""################################################Get the flight data################################################"""
hpstat1 = stat_1_conv[0]
Vcstat1 = stat_1_conv[1]
Alpha1 = stat_1_conv[2]
FFLstat1 = stat_1_conv[3]
FFRstat1 = stat_1_conv[4]
Tstat1 = stat_1_conv[6]

hpstat2 = stat_2_conv[0]
Vcstat2 = stat_2_conv[1]
Alpha2 = stat_2_conv[2]
FFLstat2 = stat_2_conv[6]
FFRstat2 = stat_2_conv[7]
Tstat2 = stat_2_conv[9]


print (stat_1_conv)
"""################################################Get the stationary values and make lists################################################"""
ii = 0
for ii in range (numberdatasets): 
    if ii == 1: 
        Vc = Vcstat1
    else:
        Vc = Vcstat2
    i = 0 
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
    
print (Mlist)
"""################################################Make the thrust file################################################"""
i = 0
file = open("matlab.dat", "w") 


for i in range(6):
    TISA.append(Tstat1[i] + llambda * hpstat1[1][i])

Tempdiff1 = Tlist - TISA


for i in range(6):  
    file.write( str(hpstat1[1][i]) + " " )
    file.write( str(Mlist[i]) + " " )
    file.write( str(Tempdiff1[i]) + " " )
    file.write( str(FFLstat1[1][i]) + " " )
    file.write( str(FFRstat1[1][i]) + "\n"  )
    
for i in range(6):  
    file.write( str(hpstat2[1][i]) + " " )
    file.write( str(Mlist[i+4]) + " " )
    file.write( str(Tempdiff2[i]) + " " )
    file.write( str(FFLstat2[1][i]) + " " )
    file.write( str(FFRstat2[1][i]) + "\n"  )
 
file.close()


"""################################################Get output State system Symmetric################################################"""
#ss_sym(muclist[0], c, V_TASlist[0], Cmadot, KY2, Cxu, CXa, CZ0, CXq, CZu, CZa, CX0, Czq, Cmu, Cma, Cmq, CXde, CZde, Cmde)

