# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:00:04 2019

@author: mathi
"""
from Constants import *
import control.matlab as control
import numpy as np
from math import *
import matplotlib.pyplot as plt

def ss_sym():
    
    C1 = np.matrix([[-2*muc*(c/V0), 0.,0.,0.],
                     [0., (CZadot - 2*muc)*(c/V0), 0., 0.],
                     [0.,0.,-(c/V0), 0.],
                     [0., Cmadot*(c/V0), 0., -2*muc*KY2*(c/V0)**2]])

    C2 = np.matrix([[CXu, CXa, CZ0, CXq*(c/V0)],
                    [CZu, CZa, -CX0, (CZq + 2*muc)*(c/V0)],
                    [0.,0.,0.,1*(c/V0)],
                    [Cmu, Cma, 0., Cmq*(c/V0)]])
    
    C3 = np.matrix([[CXde],
                    [CZde],
                    [0.],
                    [Cmde]])
    
    Cs = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
    
    Ds = np.matrix([[0.],[0.],[0.],[0.]])
    
    As = np.dot(-np.linalg.inv(C1),C2)
    Bs = np.dot(-np.linalg.inv(C1),C3)
    
    
    sys = control.ss(As,Bs,Cs,Ds)
    eigs = np.linalg.eig(sys.A)
    
    tryinput=-0.005
    t1 = np.arange(0,10,0.01)
    t2 = np.arange(0,150,0.01)
    U1 = np.ones(len(t1))*tryinput
    U2 = np.ones(len(t2))*tryinput

    y1,t1,x1 = control.lsim(sys, U1, t1)
    y2,t2,x2 = control.lsim(sys, U2, t2)

#defining arrays of the different state variables for the short period motion
    y_u_1 = []
    y_alpha_1=[]
    y_theta_1 = []
    y_q_1 = []
    y_V_1 = []
#defining arrays of the different state variable for the phugoid motion    
    y_u_2 = []
    y_alpha_2=[]
    y_theta_2 = []
    y_q_2 = []
    y_V_2 = []
    
    for i in range(len(y1)):
        y_u_1.append(y1[i][0])
        y_alpha_1.append(y1[i][1])
        y_theta_1.append(y1[i][2])
        y_q_1.append(y1[i][3])
        y_V_1.append(y1[i][0]+V0)
        
    for i in range(len(y2)):
        y_u_2.append(y2[i][0])
        y_alpha_2.append(y2[i][1])
        y_theta_2.append(y2[i][2])
        y_q_2.append(y2[i][3])
        y_V_2.append(y2[i][0]+V0)
#    print(y_u)
#    print(y_V)
    print(y_theta_1)
    print(y_theta_2)
    print(eigs[0])
    
# plots for the short period motion
    plt.subplot(2,2,1)
    plt.plot(t1,y_V_1)
    plt.title('Response of the speed due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('V[m/sec]')
    
    plt.subplot(2,2,2)
    plt.plot(t1,y_alpha_1)
    plt.title('Response of the angle of attack due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('$a$[Rad]')
    
    plt.subplot(2,2,3)
    plt.plot(t1,y_theta_1)
    plt.title('Response of $\theta$ due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('$\ Theta$[Rad]')

    plt.subplot(2,2,4)
    plt.plot(t1,y_q_1)
    plt.title('Response of pitch rate (q) due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('q[Rad/sec]') 

#plots for the phugoid
    plt.subplot(2,2,1)
    plt.plot(t2,y_V_2)
    plt.title('Response of the speed due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('V[m/sec]')
    
    plt.subplot(2,2,2)
    plt.plot(t2,y_alpha_2)
    plt.title('Response of the angle of attack due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('$a$[Rad]')
    
    plt.subplot(2,2,3)
    plt.plot(t2,y_theta_2)
    plt.title('Response of $\theta$ due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('$\ Theta$[Rad]')

    plt.subplot(2,2,4)
    plt.plot(t2,y_q_2)
    plt.title('Response of pitch rate (q) due to elevator deflection')
    plt.xlabel('t[sec]')
    plt.ylabel('q[Rad/sec]')   
    plt.show()
    
