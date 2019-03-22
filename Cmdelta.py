# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:01:31 2019

@author: mathi
"""
from Constants import *
#import W, rho, V_TAS at time of changing the cg position
#import cg shift
#import ddelta shift 
from import_ref_data import *
from cog2 import *
from CombinedProgram import rho_xcg1, W_xcg1, V_TAS_xcg1

def Cmdelta():
    
    fl = startfuelmass - stat_xcg[8][1][0][0]
    delta1 = stat_xcg[3][1][0][0]
    delta2 = stat_xcg[3][1][1][0]
    cg1 = cg(fl)[0]
    cg2 = cg(fl)[1]
    dcg = cg2-cg1
    ddelta = delta2-delta1
    CN = 2*W_xcg1/(rho_xcg1*V_TAS_xcg1*V_TAS_xcg1*S)
    Cmde = -(1/(ddelta*pi/180))*CN*(dcg/c)
    print(cg1)
    print(cg2)
    return Cmde