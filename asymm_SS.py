#!/usr/bin/enV_TAS python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: Mathilde Terleth
"""
#from Constants import *
from Constants import *
import numpy as np
import numpy.linalg as la
import control.matlab as control
import matplotlib.pyplot as plt
from import_ref_data import show_eigmot_names,get_eigmot

#'Aper. Roll', 'Dutch Roll', 'Dutch Roll YD', 'Spiral'

name = 'Spiral'

V_TAS = get_eigmot(name)[0]
mass = get_eigmot(name)[1]
rho = get_eigmot(name)[2]
roll_angle = get_eigmot(name)[12]
p_0 = get_eigmot(name)[13]
r_0 = get_eigmot(name)[14]
rudder_int = np.array(get_eigmot(name)[15])
aileron_int = np.array(get_eigmot(name)[16])

rudder_int = rudder_int - rudder_int[0]
aileron_int = aileron_int - aileron_int[0]

roll_int = get_eigmot(name)[17]
p_int = get_eigmot(name)[18]
r_int = get_eigmot(name)[19]



def Asymm_SS():
    
    W = mass*g
    CL = 2*W/(rho*V_TAS*V_TAS*S)
    
    mub =  mass / (rho * S * b)

    #dimensionless
    C11 = np.matrix([[(CYbdot-2*mub)*(b/V_TAS), 0, 0, 0],
           [0, -1/2*(b/V_TAS), 0, 0],
           [0, 0, -4*mub*KX2*(b**2/(2*V_TAS**2)), 4*mub*KXZ*(b**2/(2*V_TAS**2))],
           [Cnbdot*(b/V_TAS), 0, 4*mub*KXZ*(b**2/(2*V_TAS**2)), -4*mub*KZ2*(b**2/(2*V_TAS**2))]])
    
    C22 = np.matrix([[CYb, CL, CYp*(b/(2*V_TAS)), (CYr-4*mub)*(b/(2*V_TAS))],
           [0, 0, 1.*(b/(2*V_TAS)), 0],
           [Clb, 0, Clp*(b/(2*V_TAS)), Clr*(b/(2*V_TAS))],
           [Cnb, 0, Cnp*(b/(2*V_TAS)), Cnr*(b/(2*V_TAS))]])
    
    C33 = np.matrix([[CYda, CYdr],
          [0, 0],
          [Clda, Cldr],
          [Cnda, Cndr]])

    A = -la.inv(C11)*C22
    B = -la.inv(C11)*C33
    C = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
    D = np.matrix([[0., 0.],[0., 0.],[0., 0.],[0., 0.]])
    
    sys = control.ss(A,B,C,D)
    eigs = np.linalg.eig(sys.A)
    eigsdim = eigs[0]*(V_TAS/b)
    
    print(eigs[0])
    
    realpart = eigs[0].real
    imagpart = eigs[0].imag
    Period=[]
    HalfT = []
    Dampratio = []
    for i in range(len(realpart)):
        P= ((2*pi)/(imagpart[i]))*(b/V_TAS)
        Period.append(P)
        Thalf= (log(1/2)/realpart[i])*(b/V_TAS)
        HalfT.append(Thalf)
        Damp = -realpart[i]/(realpart[i]**2 + imagpart[i]**2)**0.5
        Dampratio.append(Damp)
        
    print(Period)
    print(HalfT)
    print(Dampratio)
        
    rudinput = rudder_int
    aleinput = aileron_int
    if name == 'Spiral':
        
        t1 = np.arange(0, 150, 0.1)
        U_rudder = np.ones(len(t1))*rudinput 
        U_aileron = np.ones(len(t1))*aleinput
        U_tot = np.vstack((U_aileron,U_rudder))
    if name == 'Aper. Roll' or name == 'Dutch Roll':
        t1 = np.arange(0, 15, 0.1)
        U_rudder = np.ones(len(t1))*rudinput 
        U_aileron = np.ones(len(t1))*aleinput
        U_tot = np.vstack((U_aileron,U_rudder))

    
    y,t,x = control.lsim(sys, U_tot.T, t1)

#defining arrays of the different state variables for the short period motion
    y_aileron = []
    y_rudder = []
    y_beta=[]   #sideslip angle
    y_phi = [] #roll angle
    y_p = []  #roll rate
    y_r = [] #yaw rate
        
    for i in range(len(y)):
        y_aileron.append(aileron_int[i])
        y_rudder.append(rudder_int[i])
        y_beta.append(y[i][0])
        y_phi.append(y[i][1] + roll_angle)
        y_p.append(y[i][2] + p_0)
        y_r.append(y[i][3]+ r_0)
        
            
    # plots for the short period motion
    
    plt.subplot(5,1,1)
    plt.plot(t, y_aileron)
    plt.plot(t, y_rudder, 'r--')
    plt.title('Aileron and rudder eflection')
    plt.xlabel('t[sec]')
    plt.ylabel('\u03B4 and \u03B4  [Rad]')
    
    plt.subplot(5,1,2)
    plt.plot(t,y_beta)
    plt.title('Response of side slip angle due to')
    plt.xlabel('t[sec]')
    plt.ylabel('beta [Rad]')
    
    plt.subplot(5,1,3)
    plt.plot(t,y_phi, 'b-')
    plt.plot(t,roll_int, 'r--')
    plt.title('Response of roll angle due to ')
    plt.xlabel('t[sec]')
    plt.ylabel('phi [Rad]')
    
    plt.subplot(5,1,4)
    plt.plot(t,y_p)
    plt.plot(t, p_int, 'r--')
    plt.title('Response of roll rate due to ')
    plt.xlabel('t[sec]')
    plt.ylabel('p [Rad/sec]')

    plt.subplot(5,1,5)
    plt.plot(t,y_r)
    plt.plot(t,r_int, 'r--')
    plt.title('Response of yaw rate due to ')
    plt.xlabel('t[sec]')
    plt.ylabel('r [Rad/sec]') 
    
    plt.show()    
          
    return mub,CL

#plt.plot(t,y)

#V_TAS = V_TAS_TAS = 3.
#mub = 19.
#CL = 5.
#
#
#yb = V_TAS/b * CYb / (2*mub)
#yphi = V_TAS/b * CL / (2*mub)
#yp = V_TAS/b * CYp / (2*mub)
#yr = V_TAS/b * (CYr-4*mub)/(2*mub)
#yda = V_TAS/b * CYda/(2*mub)
#ydr = V_TAS/b * CYdr/(2*mub)
#
#lb = V_TAS/b * (Clb*KZ2+Cnb*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#lphi = 0
#lp = V_TAS/b * (Clp*KZ2+Cnp*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#lr = V_TAS/b * (Clr*KZ2+Cnr*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#lda = V_TAS/b * (Clda*KZ2+Cnda*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#ldr = V_TAS/b * (Cldr*KZ2+Cndr*KXZ) / (4*mub*(KX2*KZ2-KXZ**2))
#
#nb = V_TAS/b * (Clb*KXZ+Cnb*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#nphi = 0
#n_p = V_TAS/b * (Clp*KXZ+Cnp*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#nr = V_TAS/b * (Clr*KXZ+Cnr*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#nda = V_TAS/b * (Clda*KXZ+Cnda*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#ndr = V_TAS/b * (Cldr*KXZ+Cndr*KX2) / (4*mub*(KX2*KZ2-KXZ**2))
#
#dim = b/(2*V_TAS)
#
#Aa = np.matrix([[yb, yphi, yp*dim, yr*dim],\
#                [0, 0, 2*V_TAS/b*dim, 0*dim],\
#                [lb, 0, lp*dim, lr*dim],\
#                [nb, 0, n_p*dim, nr*dim]])
#Ba = np.matrix([[0, ydr],\
#                [0, 0],\
#                [lda, ldr],\
#                [nda, ndr]])
#
#Ca = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
#Da = np.matrix([[0., 0.],[0., 0.],[0., 0.],[0., 0.]])
#
#sys_as = control.ss(Aa,Ba,Ca,Da)
#eigw_as, eigv_as = la.eig(sys_as.A) #eigenV_TASalues & eigenV_TASectors of A-matrix (asymmetric)
#print(eigw_as)