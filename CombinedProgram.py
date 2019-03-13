# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:55:35 2019

@author: Mathieu D'heer
"""

from Constants import * 
from StationaryValues import * 
from ss_sym import * 
import sys, string, os
#from asymm_SS import * 
ThrustUpdate = False

"""################################################Parameters defined################################################"""
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
TISA1 = []
TISA2 = []
Tempdiff1 = []
Tempdiff2 = []
ThrustStat1FD = []
ThurstStat2FD = []
ThurstStat1G = []
ThrustStat2G = []
mlist =[]                    # mass [kg]


th   =  [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # pitch angle in the stationary flight condition [rad] (given)
#TISA = [246.20300399999996, 244.22281599999997, 242.92281599999995, 240.94262799999996, 239.52281599999998, 238.52281599999998] #Temperature Corrected
# Aircraft mass
m = [4000.,4000.,4000.,4000.,4000.,4000.]      


"""################################################Get the flight data################################################"""
hpstat1 = stat_1_conv[0]
Vcstat1 = stat_1_conv[1]
Alpha1 = stat_1_conv[2]
Tstat1 = stat_1_conv[6]
FFLstat1 = stat_1_conv[3]
FFRstat1 = stat_1_conv[4]
FFFLstat1 = FFFRstat1 = FFFLstat2 = FFFRstat2 = [0.048,0.048,0.048,0.048,0.048,0.048]
for i in range(6):
    mlist.append(stat_mass(stat_1_conv[5][i][0]))

hpstat2 = stat_2_conv[0]
Vcstat2 = stat_2_conv[1]
Alpha2 = stat_2_conv[2]
Tstat2 = stat_2_conv[9]
FFLstat2 = stat_2_conv[6]
FFRstat2 = stat_2_conv[7]

for i in range(6):
    mlist.append(stat_mass(stat_1_conv[8][i][0]))
    
print (mlist)

"""################################################Get the stationary values and make lists################################################"""
#The format is: [a, b, c, d, e, f, g, h, i, j, k, l]. The first 6 are the values from the first test, the last 6 are the one of the final test.
for i in range(datalength): 
    p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve, a = StationaryValues(hpstat1[1][i][0], Tstat1[1][i][0], Vcstat1[1][i][0], m[i], th[i])
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
for i in range(datalength): 
    p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve, a = StationaryValues(hpstat2[1][i][0], Tstat2[1][i][0], Vcstat2[1][i][0], m[i], th[i])
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


"""################################################Make the thrust file################################################"""
#Must be in format the pressure altitude,  the Mach number,  the temperature difference,
#the fuel flow of the left jet engine,  the fuel flow of the right jet engine. 
file = open("matlab.dat", "w") 

#Calculates temperature difference. 
for i in range(6):
    TISA1.append(Tstat1[1][i][0] + llambda * hpstat1[1][i][0])
    TISA2.append(Tstat2[1][i][0] + llambda * hpstat2[1][i][0])
    Tempdiff1.append(Tlist[i] - TISA1[i])
    Tempdiff2.append(Tlist[i-5] - TISA2[i])

#Prints the first 6 lines for the first test.
for i in range(6):  
    file.write( str(hpstat1[1][i][0]) + " " )
    file.write( str(Mlist[i]) + " " )
    file.write( str(Tempdiff1[i]) + " " )
    file.write( str(FFLstat1[1][i][0]) + " " )
    file.write( str(FFRstat1[1][i][0]) + "\n" )
#Prints the second 6 lines for the second test.

for i in range(6):  
    file.write( str(hpstat2[1][i][0]) + " " )
    file.write( str(Mlist[i+4]) + " " )
    file.write( str(Tempdiff2[i]) + " " )
    file.write( str(FFLstat2[1][i][0]) + " " )
    file.write( str(FFRstat2[1][i][0]) + "\n" )
 
    
#Prints the first 6 lines for the first test with the fixed fuelflow.
for i in range(6):  
    file.write( str(hpstat1[1][i][0]) + " " )
    file.write( str(Mlist[i]) + " " )
    file.write( str(Tempdiff1[i]) + " " )
    file.write(str(FFFLstat1[i]) + " " )
    file.write(str(FFFRstat1[i]) + "\n" )
#Prints the second 6 lines for the second test with the fixed fuel flow.

for i in range(6):  
    file.write( str(hpstat2[1][i][0]) + " " )
    file.write( str(Mlist[i+4]) + " " )
    file.write( str(Tempdiff2[i]) + " " )
    file.write(str(FFFLstat2[i]) + " " )
    file.write(str(FFFRstat2[i]) + "\n" )
    
    
    
    
file.close()
#Update Thrust File
if ThrustUpdate == True :
    os.startfile("thrust(1).exe")

"""################################################Take the thrust file and put the values in a list################################################"""


for i in range(12):
    ThrustStat1FD.append(Thrustresult[i])
    ThurstStat2FD.append(Thrustresult[i + 12])
    ThurstStat1G.append(Thrustresult[i + 24])
    ThrustStat2G.append(Thrustresult[i + 36])

print(ThrustStat2G)
"""################################################Get output State Space Symmetric################################################"""
Sym_SS(V_TAS, muc, CX0, CZ0, rho)

"""################################################Get output State Space Assymmetric################################################"""
Asymm_SS(V_TASlist[0], mub[0])





