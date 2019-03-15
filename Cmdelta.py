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
from cog import *
from CombinedProgram import rho_xcg1, W_xcg1, V_TAS_xcg1, rho_xcg2, W_xcg2
print(W_xcg1)
print(W_xcg2)

def Cmdelta():
    
    fl1 = startfuelmass - stat_xcg[8][1][0][0]
    fl2 = starfuelmass - stat_xcg[8][1][1][0]
    delta1 = stat_xcg[3][1][0][0]
    delta2 = stat_xcg[3][1][1][0]
    cg1 = cg(fl1)[0]
    cg2 = cg(fl2)[1]
    dcg = cg1-cg2
    ddelta = delta1-delta2
    CN = 2*W/(rho*V_TAS*V_TAS*S)
    Cmdelta = -(1/ddelta)*CN*(dcg/c)
    
    return Cmdelta