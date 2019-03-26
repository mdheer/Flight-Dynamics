#!/usr/bin/enV_TAS python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:50:11 2019

@author: Mathilde Terleth
"""

from Constants import *
import numpy as np
import numpy.linalg as la
import control.matlab as control
import matplotlib.pyplot as plt
from import_ref_data import show_eigmot_names,get_eigmot

#'Aper. Roll', 'Dutch Roll', 'Dutch Roll YD', 'Spiral'

name = 'Aper. Roll'

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
    eigsdimless = eigs[0]/(V_TAS/b)
    
    print(eigs[0])
    print(eigsdimless)
    print(b)
    print(V_TAS)
    realpart = eigsdimless.real
    imagpart = eigsdimless.imag
    Period=[]
    HalfT = []
    Dampratio = []
    for i in range(len(realpart)):
        P= ((2*pi)/(imagpart[i]))*(b/V_TAS)
        Period.append(P)
        Thalf= (log(1/2)/realpart[i])*(b/V_TAS)
        print(realpart[i])
        HalfT.append(Thalf)
        Damp = -realpart[i]/(realpart[i]**2 + imagpart[i]**2)**0.5
        Dampratio.append(Damp)
        
    print(Period)
    print(HalfT)
    print(Dampratio)
        
    rudinput = rudder_int
    aleinput = aileron_int
    
    initial=False
    
    if initial==True:
        
        beta = 0#radians(2)
        phi = radians(2)
        p = 0.
        r = 0#radians(2)
        
        X0 = np.array([beta, phi, p ,r])
        t = np.arange(0, 30, 0.1)
        y,t = control.initial(sys, t, X0)

        
        y_beta=[]   #sideslip angle
        y_phi = [] #roll angle
        y_p = []  #roll rate
        y_r = [] #yaw rate
            
        for i in range(len(y)):
            y_beta.append(degrees(y[i][0]))
            y_phi.append(degrees(y[i][1]))
            y_p.append(degrees(y[i][2]))
            y_r.append(degrees(y[i][3]))
            
                
        # PLOTTING
        
        plt.subplot(2,2,1)
        plt.plot(t,y_beta, 'b-')
        plt.title('Side slip angle', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('\u03B2 [deg]')
        
        plt.subplot(2,2,2)
        plt.plot(t,y_phi, 'b-')
        plt.title('Roll angle', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('\u03C6 [deg]')
        
        plt.subplot(2,2,3)
        plt.plot(t,y_p, 'b-')
        plt.title('Roll rate', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('p [deg/sec]')
    
        plt.subplot(2,2,4)
        plt.plot(t,y_r, 'b-')
        plt.title('Yaw rate', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('r [deg/sec]') 
        
        plt.show()    
    
    elif initial ==False:
        
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
            y_aileron.append(degrees(aileron_int[i]))
            y_rudder.append(degrees(rudder_int[i]))
            y_beta.append(-degrees(y[i][0]))
            y_phi.append(-degrees(y[i][1]) + degrees(roll_angle))
            y_p.append(-degrees(y[i][2]) + degrees(p_0))
            y_r.append(-degrees(y[i][3]) + degrees(r_0))
            
                
        # PLOTTING
        
        # Labels to use in the legend for each line
        
#        fig= plt.figure()
        
        plt.subplot(4,1,1)
        plt.plot(t, y_aileron,'g-', label="Aileron deflection")
        plt.plot(t, y_rudder, 'k-', label="Rudder deflection")
        plt.title('Aileron and rudder deflection')
        plt.xlabel('t[sec]')
        plt.ylabel('\u03B4a and \u03B4r  [Rad]')
        plt.grid()
        plt.legend(bbox_to_anchor=(1.0,0.5))
        
#        plt.subplot(5,1,2)
#        plt.plot(t,y_beta, 'b-',)
#        plt.title('Side slip angle', fontweight="bold")
#        plt.xlabel('t [sec]')
#        plt.ylabel('\u03B2 [deg]') 
#        plt.grid()
        
        plt.subplot(4,1,2)
        l3 = plt.plot(t,y_phi, 'b-', label="Numerical model")
        l4 = plt.plot(t,roll_int, 'r--', label="Flight test")
        plt.title('Roll angle', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('\u03C6 [deg]')
        plt.grid()
        plt.legend(bbox_to_anchor=(1.0, 1.0))
        
        plt.subplot(4,1,3)
        plt.plot(t,y_p, 'b-')
        plt.plot(t, p_int, 'r--')
        plt.title('Roll rate', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('p [deg/sec]')
        plt.grid()
        
        plt.subplot(4,1,4)
        plt.plot(t,y_r,'b-')
        plt.plot(t,r_int, 'r--')
        plt.title('Yaw rate', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('r [deg/sec]') 
        plt.grid()
        
        plt.show()    
        
        Phi_descre_tot = []
        P_descre_tot = []
        R_descre_tot = []
        
        for i in range(len(t)):
            Phi_descre_tot.append(abs(y_phi[i] - roll_int[i]))
            P_descre_tot.append(abs(y_p[i] - p_int[i]))
            R_descre_tot.append(abs(y_r[i] - r_int[i]))
        
        Phi_descre_av = np.average(Phi_descre_tot)
        P_descre_av = np.average(P_descre_tot)
        R_descre_av = np.average(R_descre_tot)
        
        print(Phi_descre_av)
        print(P_descre_av)
        print(R_descre_av)
        print(mub)
        print(mass)
        print(V_TAS)
        return mub,CL

#Simul = Asymm_SS()