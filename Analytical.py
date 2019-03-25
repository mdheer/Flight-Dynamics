# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:15:20 2019

@author: mathi
"""
import numpy as np
from Constants import *
from ss_sym import *
from asymm_SS import *

mub = Asymm_SS()[0]
CL = Asymm_SS()[1]
muc = Sym_SS()[0]
CZ0 = Sym_SS()[1]
CX0 = Sym_SS()[2]


A_sp = 4*muc*muc*KY2
B_sp = -2*muc*(KY2*CZa + Cmadot + Cmq)
C_sp = CZa*Cmq - 2*muc*Cma

A_phu = 2*muc*(CZa*Cmq - 2*muc*Cma)
B_phu = 2*muc*(CXu*Cma - Cmu*CXa) + Cmq*(CZu*CXa - CXu*CZa)
C_phu = CZ0*(Cmu*CZa - CZu*Cma)

A_dr= 8*mub*mub*KZ2
B_dr = -2*mub*(Cnr + 2*KZ2*CYb)
C_dr = 4*mub*Cnb + CYb*Cnr

eig_aperiodic = Clp/(4*mub*KX2)

eig_spiral = (2*CL*(Clb*Cnr - Cnb*Clr))/(Clp*(CYb*Cnr + 4*mub*Cnb) - Cnp*(CYb*Clr + 4*mub*Clb))

eig_sp = (-B_sp + 1j*np.sqrt(4*A_sp*C_sp - B_sp*B_sp))/(2*A_sp)
eig_phu= (-B_phu + 1j*np.sqrt(4*A_phu*C_phu - B_phu*B_phu))/(2*A_phu)
eig_dr= (-B_dr + 1j*np.sqrt(4*A_dr*C_dr - B_dr*B_dr))/(2*A_dr)

eigs = [eig_sp, eig_phu, eig_aperiodic, eig_dr, eig_spiral]

realpart = eigs[0].real
imagpart = eigs[0].imag

#for the symmetric cases
P= ((2*pi)/(imagpart))*(c/V_TAS)
Thalf= (log(1/2)/realpart)*(c/V_TAS)
print(b)
print(V_TAS)
#for the asymmetric cases
#P= ((2*pi)/(imagpart))*(b/V_TAS)
#Thalf= (log(1/2)/realpart)*(b/V_TAS)


Damp = -realpart/(realpart**2 + imagpart**2)**0.5


print('Period = ', P)
print('Thalf =', Thalf)
print('Damping =', Damp)

print(eig_sp)
#print(eig_phu)
#print(eig_aperiodic) 
#print(eig_dr)
#print(eig_spiral)

