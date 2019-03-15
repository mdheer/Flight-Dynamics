
from Constants import * 
from StationaryValues import * 
#from ss_sym import * 
import sys, string, os
from import_ref_data import *
#from asymm_SS import * 


""" ============== I. General Output Parameters ============== """

ThrustUpdate = True
PrintSSEigenvalues = True
PrintASSEigenvalues = True


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
de_meas = stat_2_conv[3][1]
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


""" ============== V. Make the thrust file ============== """

# Must be in format the pressure altitude,  the Mach number,  the temperature difference,
# the fuel flow of the left jet engine,  the fuel flow of the right jet engine. 

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

for i in range(12):
    ThrustStat1FD.append(Thrustresult[i])
    ThurstStat2FD.append(Thrustresult[i + 12])
    ThurstStat1G.append(Thrustresult[i + 24])
    ThrustStat2G.append(Thrustresult[i + 36])



""" ============== VII. CL and CD calculation ============== """





""" ============== VIII. Get output State Space Symmetric ============== """


#Sym_SS(V_TAS, muc, CX0, CZ0, rho, PrintSSEigenvalues)




""" ============== XI. Get output State Space Assymmetric ============== """

#Asymm_SS(V_TASlist[0], mub)

#Asymm_SS(V_TASlist[7], mublist[7], PrintASSEigenvalues)



