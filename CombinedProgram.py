import numpy as np
from Constants import * 
from StationaryValues import * 
#from ss_sym import * 
import sys, string, os
from import_ref_data import *
#from asymm_SS import * 

import matplotlib.pyplot as plt

Ws = 60500. # Standard aircraft mass [N] 
Cmtc = -0.0064

"""################################################General Output Parameters################################################"""

""" ============== I. General Output Parameters ============== """

ThrustUpdate = True
PrintSSEigenvalues = True
Calcasymm_SS = True

""" ============== II. Parameters defined ============== """

#datalength = 6
numberdatasets = 2

plist1 = []
plist2 = []

rholist1 = []
rholist2 = []

Mlist1 = []
Mlist2 = []

Tlist1 = []
Tlist2 = []

Wlist1 = []
Wlist2 = []

V_TASlist1 = []
V_TASlist2 = []

Velist1 = []
Velist2 = []

alist1 = []
alist2 = []

TISA1 = []
TISA2 = []

Tempdiff1 = []
Tempdiff2 = []

ThrustStat1FD = []
ThurstStat2FD = []

ThurstStat1G = []
ThrustStat2G = []

mlist1 = []
mlist2 = []


#th   =  [1.8, 2.5, 3.3, 5.2, 8., 10.5]                  # pitch angle in the stationary flight condition [rad] (given)
#TISA = [246.20300399999996, 244.22281599999997, 242.92281599999995, 240.94262799999996, 239.52281599999998, 238.52281599999998] #Temperature Corrected
# Aircraft mass


"""  ============== III. Get the flight data ============== """

hpstat1 = stat_1_conv[0][1]
Vcstat1 = stat_1_conv[1][1] - 2.
Alpha1 = stat_1_conv[2][1]
Tstat1 = stat_1_conv[6][1]
FFLstat1 = stat_1_conv[3][1]
FFRstat1 = stat_1_conv[4][1]
FFFLstat1 = FFFRstat1 = FFFLstat2 = FFFRstat2 = [0.048,0.048,0.048,0.048,0.048,0.048,0.048]


for i in range(len(stat_1_conv[5][1])):
    mlist1.append(stat_mass(stat_1_conv[5][1][i][0]))



hpstat2 = stat_2_conv[0][1]
Vcstat2 = stat_2_conv[1][1] - 2.
Alpha2 = stat_2_conv[2][1]
de_meash = stat_2_conv[3][1]
F_meas = stat_2_conv[5][1]
Tstat2 = stat_2_conv[9][1]
FFLstat2 = stat_2_conv[6][1]
FFRstat2 = stat_2_conv[7][1]

for i in range(len(stat_2_conv[8][1])):
    mlist2.append(stat_mass(stat_2_conv[8][1][i][0]))
    
    
""" ============== IV. Get the stationary values and make lists ============== """

# The format is: [a, b, c, d, e, f, g, h, i, j, k, l]. The first 6 are the values from the first test, the last 6 are the one of the final test.

for i in range(len(stat_1_conv[0][1])): 
    
    p, rho, M, T, W, V_TAS, Ve, a = StationaryValues(hpstat1[i][0], Tstat1[i][0], Vcstat1[i][0], mlist1[i])
    
    plist1.append(p)
    rholist1.append(rho)
    Mlist1.append(M)
    Tlist1.append(T)
    Wlist1.append(W)
    V_TASlist1.append(V_TAS)
    Velist1.append(Ve)
    alist1.append(a)

for i in range(len(stat_2_conv[0][1])): 
    
    p, rho, M, T, W, V_TAS, Ve, a = StationaryValues(hpstat2[i][0], Tstat2[i][0], Vcstat2[i][0], mlist2[i])
    
    plist2.append(p)
    rholist2.append(rho)
    Mlist2.append(M)
    Tlist2.append(T)
    Wlist2.append(W)
    V_TASlist2.append(V_TAS)
    Velist2.append(Ve)
    alist2.append(a)

#calculate these values for first cg position (xcg1)
p_xcg1, rho_xcg1, M_xcg1, T_xcg1, W_xcg1, V_TAS_xcg1, Ve_xcg1, a_xcg1 = StationaryValues(stat_xcg_conv[0][1][0][0], stat_xcg_conv[9][1][0][0], stat_xcg_conv[1][1][0][0]-2, stat_mass(stat_xcg_conv[8][1][0][0]))

""" ============== V. Make the thrust file ============== """

# Must be in format the pressure altitude,  the Mach number,  the temperature difference,
# the fuel flow of the left jet engine,  the fuel flow of the right jet engine. 
if ThrustUpdate == True: 
    file = open("matlab.dat", "w") 
    
    #Calculates temperature difference for first and second test respectively. 
    for i in range(len(stat_1_conv[0][1])):
        
        TISA1.append(Tstat1[i][0] + llambda * hpstat1[i][0])
        Tempdiff1.append(Tlist1[i] - TISA1[i])
        
    for i in range(len(stat_2_conv[0][1])): 
        TISA2.append(Tstat2[i][0] + llambda * hpstat2[i][0])   
        Tempdiff2.append(Tlist2[i] - TISA2[i])
    
    #Prints the first 6 lines for the first test.
    for i in range(len(stat_1_conv[0][1])):
        
        file.write( str(hpstat1[i][0])  + " " )
        file.write( str(Mlist1[i])      + " " )
        file.write( str(Tempdiff1[i])   + " " )
        file.write( str(FFLstat1[i][0]) + " " )
        file.write( str(FFRstat1[i][0]) + "\n")
        
    #Prints the second 6 lines for the second test.
    for i in range(len(stat_2_conv[0][1])):  
        
        file.write( str(hpstat2[i][0])  + " " )
        file.write( str(Mlist2[i])      + " " )
        file.write( str(Tempdiff2[i])   + " " )
        file.write( str(FFLstat2[i][0]) + " " )
        file.write( str(FFRstat2[i][0]) + "\n")
        
    #Prints the first 6 lines for the first test with the fixed fuelflow.
    for i in range(len(stat_1_conv[0][1])):  
        
        file.write( str(hpstat1[i][0]) + " " )
        file.write( str(Mlist1[i])     + " " )
        file.write( str(Tempdiff1[i])  + " " )
        file.write( str(FFFLstat1[i])  + " " )
        file.write( str(FFFRstat1[i])  + "\n")
        
        
    #Prints the second 6 lines for the second test with the fixed fuel flow.
    for i in range(len(stat_2_conv[0][1])):  
        file.write( str(hpstat2[i][0]) + " " )
        file.write( str(Mlist2[i])     + " " )
        file.write( str(Tempdiff2[i])  + " " )
        file.write( str(FFFLstat2[i])  + " " )
        file.write( str(FFFRstat2[i])  + "\n")
           
    file.close()
    
    #Update Thrust File
    if ThrustUpdate == True :
        os.startfile("thrust(1).exe")
    

    """ ============== VI. Take the thrust file and put the values in a list ============== """
    
    for i in range(len(stat_1_conv[0][1])*2):
        ThrustStat1FD.append(float(Thrustresult[i]))          # L - R - L - R etc.
        ThurstStat1G.append(float(Thrustresult[i + len(stat_1_conv[0][1])*4]))
    
    for i in range(len(stat_2_conv[0][1])*2):
        ThurstStat2FD.append(float(Thrustresult[i + len(stat_2_conv[0][1])*2]))
        ThrustStat2G.append(float(Thrustresult[i + len(stat_2_conv[0][1])*2+len(stat_1_conv[0][1])*4]))

""" ============== VII. CL and CD calculation ============== """


#print(len(ThurstStat2FD))

""" ============== VIII. Get output State Space Symmetric ============== """

    
#Sym_SS(V_TAS, muc, CX0, CZ0, rho, PrintSSEigenvalues)



""" ============== XI. Get output State Space Assymmetric ============== """

#Asymm_SS(V_TASlist[0], mub)
#if Calcasymm_SS == True:  
#    Asymm_SS()

#print (V_TASlist1)





"""############################################### Control Force curve calculations & plot #################################"""


Fe_red = Fe_star(Ws, Wlist2, F_meas)      # Returns the reduced elevator control force in a list [N]
for i in range(len(Fe_red)):
    Fe_red[i] = Fe_red[i][0]/9.80665 

Ve_red = Ve_thilde(Velist2, Ws, Wlist2)   # Returns the reduced equivalent airspeed [m/s]

print('Ve_red = ', Ve_red)
print('Fe_red = ', Fe_red)

Fe_red_sorted = []
Ve_red_sorted = []


Fe_red.sort()
Ve_red.sort()

""" Elevator control force curve plot """

plt.plot(Ve_red, Fe_red)
plt.gca().invert_yaxis()
plt.ylabel('Reduced elevator control force [kg]')
plt.xlabel('Reduced equivalent airspeed [m/s]')
plt.show()

print('Reduced elevator control force = ', Fe_red[2])
print('Measured elevator control force = ', F_meas[2])
print('Measured weight = ', Wlist2[2])


"""############################################### Elevator trim curve #################################"""

de_meas = []
for a in range(len(de_meash)):
    de_meas.append(de_meash[a][0])

T_stan = []  # Standard thrust [N]
T_dyn = []   # Total thrust stationary measurements 2 [N]

Tcs = []    # dimensionless stationary thrust [-]
Tc = []     # dimensionless thrust [-]

b = 0
for b in range(int(len(ThrustStat2G)/2)):
    e = 2*b
    f = e + 1
    T_stan.append(ThrustStat2G[e] + ThrustStat2G[f])
    T_dyn.append(ThurstStat2FD[e] + ThurstStat2FD[f])
    b += 1 
    #print(e, f)
    
for d in range(len(rholist2)):
    Tcs.append(T_stan[d]/(0.5*1.225*V_TASlist2[d]*V_TASlist2[d]))
    Tc.append(T_dyn[d]/(0.5*rholist2[d]*V_TASlist2[d]*V_TASlist2[d]))
    
print('Tcs = ', Tcs[2])
print('Tc = ', Tc[2])   
print('measured elevator deflection = ', de_meas[2])
print('Cmtc = ', Cmtc)

de_red = []
de_red = de_star(de_meas, Cmde, Cmtc, Tcs, Tc)
print('reduced elevator deflection = ', de_red[2])

alpha2 = []     # Angle of attack during second stationary measurements
for e in range(len(Alpha2)):
    alpha2.append(Alpha2[e][0])

print('angle of attack = ', alpha2[2])
#print(de_red)
if len(Alpha2)==7:
    
    alpha2_sorted = []
    alpha2_sorted.append(alpha2[6])
    alpha2_sorted.append(alpha2[5])
    alpha2_sorted.append(alpha2[4])
    alpha2_sorted.append(alpha2[0])
    alpha2_sorted.append(alpha2[1])
    alpha2_sorted.append(alpha2[2])
    alpha2_sorted.append(alpha2[3])
    
    de_red_sorted = []
    de_red_sorted.append(de_red[6])
    de_red_sorted.append(de_red[5]) 
    de_red_sorted.append(de_red[4]) 
    de_red_sorted.append(de_red[0]) 
    de_red_sorted.append(de_red[1]) 
    de_red_sorted.append(de_red[2]) 
    de_red_sorted.append(de_red[3]) 
    
    Ve_red_sorted = []
    Ve_red_sorted.append(Ve_red[6])
    Ve_red_sorted.append(Ve_red[5]) 
    Ve_red_sorted.append(Ve_red[4]) 
    Ve_red_sorted.append(Ve_red[0]) 
    Ve_red_sorted.append(Ve_red[1]) 
    Ve_red_sorted.append(Ve_red[2])
    Ve_red_sorted.append(Ve_red[3])
    
elif len(Alpha2)==5:
    
    alpha2_sorted = []
    alpha2_sorted.append(alpha2[4])
    alpha2_sorted.append(alpha2[3])
    alpha2_sorted.append(alpha2[0])
    alpha2_sorted.append(alpha2[1])
    alpha2_sorted.append(alpha2[2])
    
    de_red_sorted = []
    de_red_sorted.append(de_red[4])
    de_red_sorted.append(de_red[3]) 
    de_red_sorted.append(de_red[0]) 
    de_red_sorted.append(de_red[1]) 
    de_red_sorted.append(de_red[2]) 
    
    Ve_red_sorted = []
    Ve_red_sorted.append(Ve_red[4])
    Ve_red_sorted.append(Ve_red[3]) 
    Ve_red_sorted.append(Ve_red[0]) 
    Ve_red_sorted.append(Ve_red[1]) 
    Ve_red_sorted.append(Ve_red[2]) 
    

 
""" Reduced elevator deflection vs Reduced equivalent velocity plot"""

#plt.plot(Ve_red_sorted, de_red_sorted)
#plt.gca().invert_yaxis()
#plt.ylabel('Reduced elevator deflection [degree]')
#plt.xlabel('Reduced equivalent airspeed [m/s]')
#plt.show()

""" Reduced elevator deflection vs Angle of attack plot(to determine Cm_alpha) """

plt.plot(alpha2_sorted, de_red_sorted)
plt.gca().invert_yaxis()
plt.ylabel('Reduced elevator deflection [degree]')
plt.xlabel('Angle of attack [degree]')
plt.show()


"""############################################### Cm_lpha (Longitudinal stability) #################################"""

Cma = (np.polyfit(alpha2_sorted, de_red_sorted, 1)[0]) * -Cmde
print(Cma)
print(np.polyfit(alpha2_sorted, de_red_sorted, 1)[0])
#print(Mlist1)