#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:00:40 2019

@author: willemvolker
"""

from Constants import c

lbs = 0.453592 #kg
inch = 0.0254 #m

xcgdat_RM = 280.31 #inch (wrt datum line, at ramp mass)
xcg = (xcgdat_RM - 261.45) * inch #m (wrt forward end of mac)
xcg_prcnt = xcg*100/c #%c

BEM = 9165*lbs #kg (basic empty mass) 
m_ramp = 14223*lbs #kg (ramp mass)
