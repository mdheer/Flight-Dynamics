
from Constants import *
from import_ref_data import *
import math

Cm0 = Cmac

def StationaryValues(hp, Tm, V_IAS, m, th):
    
    Vc = V_IAS - 2
    
    p = p0 * (1 + ((llambda*hp)/T0))**(-(g)/(llambda * R))
    
    M = sqrt((2/(gamma -1))* ((1 + (p0/p)*((1 + ((gamma -1)/(2 *gamma)) * (rho0/p0)* Vc**2)**(gamma/(gamma -1)) -1))**((gamma -1)/gamma) -1))
    
    T = Tm/(1 + ((gamma - 1)/2)* M**2)
    
    rho = p / (R*T)
    
    W = m * g
    
    muc = m / (rho * S * c)
    mub = m / (rho * S * b)
    
    a = sqrt(gamma * R * T)
    
    V_TAS = M * a
    
    Ve = V_TAS * sqrt(rho/rho0)
    
    CX0 = W * sin(rad(th)) / (0.5 * rho * V_TAS ** 2 * S)
    CZ0 = -W * cos(rad(th)) / (0.5 * rho * V_TAS ** 2 * S)
    
    return p, rho, M, T, W, muc, mub, CX0, CZ0, V_TAS, Ve, a


def DynamicValues(hp,Tm,V_IAS):
    
    hp = hp*0.3048              # [m]
    Tm = Tm+273.15              # [K]
    Vc = (V_IAS-2)*0.514444     # [m/s]
    
    p = p0 * (1 + ((llambda*hp)/T0))**(-(g)/(llambda * R))
    
    M = sqrt((2/(gamma-1)) * ((1 + (p0/p)*((1 + ((gamma-1)/(2*gamma)) * (rho0/p0)* Vc**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))
    
    T = Tm/(1+((gamma-1)/2)*M**2)
    
    rho = p / (R*T)
    
    return p,T,rho

def Ve_thilde(Ve, Ws, W):
    Ve_red = Ve * math.sqrt(Ws/W)
    return Ve_red


def de_star(Cmde, Cm0, Cma, CNwa, Cmtc, W, rho, Ve_red, Tcs, S):
    de_red = (-1./Cmde)*(Cm0 + (Cma/CNwa)*(W/(0.5 * rho * Ve_red**2 * S)) + Cmtc * Tcs)
    return de_red


def Fe_star(Ws, W, Fmeas):
    Fe_red = Fmeas * (Ws/W)
    return Fe_red  


def stat_mass(Fused):
    """ Fused = the array with fuel used, of the desired measurement. """
    """ Returns an array for total mass at that measurement moment.   """
    return total_starting_mass - Fused



# Ws = standard aircraft weight
# Ve_red = reduced equivalent airspeed
# Se = Surface area elevator
# se = stick deflection
# Chd = Ch delta
# de_red = reduced elevator deflection (for reduced trim curve)


