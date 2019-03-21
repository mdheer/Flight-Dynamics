
from Constants import *
#from import_ref_data import total_starting_mass
import math

Cm0 = Cmac

def StationaryValues(hp, Tm, Vc, m):
    
    p = p0 * (1 + ((llambda*hp)/T0))**(-(g)/(llambda * R))
    
    M = sqrt((2/(gamma -1))* ((1 + (p0/p)*((1 + ((gamma -1)/(2 *gamma)) * (rho0/p0)* Vc**2)**(gamma/(gamma -1)) -1))**((gamma -1)/gamma) -1))
    
    T = Tm/(1 + ((gamma - 1)/2)* M**2)
    
    rho = p / (R*T)
    
    W = m * g
    
    a = sqrt(gamma * R * T)
    
    V_TAS = M * a
    
    Ve = V_TAS * sqrt(rho/rho0)
    
    return p, rho, M, T, W, V_TAS, Ve, a



def DynamicValues(hp,Tm,V_IAS):
    
    hp = hp*0.3048              # [m]
    Tm = Tm+273.15              # [K]
    Vc = (V_IAS-2)*0.514444     # [m/s]
    
    p = p0 * (1 + ((llambda*hp)/T0))**(-(g)/(llambda * R))
    
    M = sqrt((2/(gamma-1)) * ((1 + (p0/p)*((1 + ((gamma-1)/(2*gamma)) * (rho0/p0)* Vc**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))
    
    T = Tm/(1+((gamma-1)/2)*M**2)
    
    rho = p / (R*T)
    
    return p,T,rho


print(DynamicValues(3600, 2, 100))

def Ve_thilde(Ve, Ws, W):
    Ve_red = []
    for i in range(len(W)):
        Ve_red.append(Ve[i] * math.sqrt(Ws/W[i]))
    return Ve_red

def de_star(de_meas, Cmd, Cmtc, Tcs, Tc):
    de_red = []
    for c in range(len(de_meas)):
        de_red.append(de_meas[c] - ((1./Cmd)*Cmtc*(Tcs[c] - Tc[c])))
    return de_red


def Fe_star(Ws, W, Fmeas):
    Fe_red = []
    for i in range(len(W)):
        Fe_red.append(Fmeas[i] * (Ws/W[i]))
    return Fe_red  







# Ws = standard aircraft weight
# Ve_red = reduced equivalent airspeed
# Se = Surface area elevator
# se = stick deflection
# Chd = Ch delta
# de_red = reduced elevator deflection (for reduced trim curve)

    
    

    
    
    