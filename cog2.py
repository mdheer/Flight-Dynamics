
""" ========== PROGRAM FOR CENTER OF GRAVITY 2 ========== """
""" ---- Adjusted to be able to calculate the values for  """
""" ---- both reference data and measured flight data. -- """

import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt

from Constants import c
from import_ref_data import total_starting_mass,weights,stat_xcg

# Conversions
lbs  = 0.453592 # [kg]
inch = 0.0254   # [m]

# ========== PART I. INTERPOLATION FUNCTION FOR FUEL MOMENTS ==========

fuelmoments = np.genfromtxt('fuelmoments.csv',delimiter=',',dtype='str')
fuelmoments = np.delete(fuelmoments,np.s_[51:],0)
    
fuel_mom_x = []
fuel_mom_y = []
    
for i in range(len(fuelmoments)-1):
    fuel_mom_x.append(float(fuelmoments[i+1][0]))
    fuel_mom_y.append(float(fuelmoments[i+1][1])*100)
    
ret_fuel_mom = interp.interp1d(fuel_mom_x,fuel_mom_y)


# ========== PART II. MASS AND BALANCE FORM ==========

def mass_and_balance(number):
    """ number==1: for starting configuration, everyone in their seats. """
    """ number==2: for cg shift configuration, person in seat 8 moves.  """
    
    # ---------- A) Payload computations ----------
    
    # Seat numbers in order according to "weights" table from "import_ref_data"
    seats          = ['1','2','9/10','3','4','5','6','7','8']
    if number==1:
        xcgdatum_seats = [131,131,170,214,214,251,251,288,288]      # [inch]
    elif number==2:
        xcgdatum_seats = [131,131,170,214,214,251,251,288,144]
    
    # Calculating moment of passengers (xcg*mass)
    pass_masses  = []
    pass_moments = []
    for i,xcg in enumerate(xcgdatum_seats):
        mass   = weights[1][0][i]/lbs   # [lbs]
        moment = mass*xcg               # [inch-lbs]
        pass_masses.append(mass)
        pass_moments.append(moment)
    
    mass_payload   = sum(pass_masses)
    moment_payload = sum(pass_moments)
    
    # ---------- B) Basic empty mass ----------
    
    xcgdatum_BEM = 292.18    # [inch]     (Given in "Mass & Balance Report")
    mass_BEM     = 9165.     # [lbs]      (Given in "Mass & Balance Report")
    moment_BEM   = 2677847.5 # [inch-lbs] (Given in "Mass & Balance Report")
    
    # ---------- C) Zero fuel mass ----------
    
    mass_ZF     = mass_payload + mass_BEM      # [lbs]
    moment_ZF   = moment_payload + moment_BEM  # [inch-lbs] 
    xcgdatum_ZF = moment_ZF / mass_ZF          # [inch]
    
    # ---------- D) Fuel load ----------
    
    # Intermezzo: interpolation function for fuel moments:
    
    mass_fuel   = weights[1][0][9]/lbs             # [lbs]
    moment_fuel = ret_fuel_mom(mass_fuel).item()   # [inch-lbs]
    
    # ---------- E) Ramp mass ----------
    
    mass_RM     = mass_ZF + mass_fuel        # [lbs]
    moment_RM   = moment_ZF + moment_fuel    # [inch-lbs]
    xcgdatum_RM = moment_RM / mass_RM        # [inch] (wrt datum line, at t0)
    
    
    xcg0       = (xcgdatum_RM-261.45)*inch      # [m] (wrt forward end of mac, at t0)
    xcg0_prcnt = xcg0*100/c                     # [%c]

    return mass_ZF,moment_ZF,mass_fuel,xcg0


# ========== PART III. CALCULATING CG SHIFT WHILE FLYING ==========

mass_ZF_1   = mass_and_balance(1)[0]
moment_ZF_1 = mass_and_balance(1)[1]

mass_ZF_2   = mass_and_balance(2)[0]
moment_ZF_2 = mass_and_balance(2)[1]

def cg(fl):
    """ Returns xcg1,xcg2 [m] wrt forward end of mac, as a function of the fuel load fl [lbs] """
    
    # Case for number==1
    mass_1     = mass_ZF_1 + fl                            # [lbs]
    moment_1   = moment_ZF_1 + ret_fuel_mom(fl).item()     # [inch-lbs]
    xcgdatum1  = moment_1/mass_1                           # [inch]
    xcg1       = (xcgdatum1-261.45)*inch                   # [m]
    xcg1_prcnt = xcg1*100/c                                # [%c ]
    
    # Case for number==2
    mass_2     = mass_ZF_2 + fl                            # [lbs]
    moment_2   = moment_ZF_2 + ret_fuel_mom(fl).item()     # [inch-lbs]
    xcgdatum2  = moment_2/mass_2                           # [inch]
    xcg2       = (xcgdatum2-261.45)*inch                   # [m]
    xcg2_prcnt = xcg2*100/c                                # [%c ]
    
    return xcg1, xcg2

# Filling in function for results:
fuel_used = stat_xcg[8][1][0].item()                     # [lbs]
mass_fuel = mass_and_balance(1)[2]                       # [lbs]
    
xcg1,xcg2 = cg(mass_fuel-fuel_used)
print()
print('xcg1 =',xcg1,'[m] wrt LEMAC')
print('xcg2 =',xcg2,'[m] wrt LEMAC')
print(xcg2-xcg1)


