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




def Cmdelta():
    
    dcg = cg1-cg2
    ddelta = delta1-delta2
    CN = 2*W/(rho*V_TAS*V_TAS*S)
    Cmdelta = -(1/ddelta)*CN*(dcg/c)
    
    return Cmdelta