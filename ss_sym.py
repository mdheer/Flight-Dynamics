# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:00:04 2019

@author: mathi
"""
#from tryreader import *
from Constants import*
import control.matlab as control
import numpy as np
from math import *
import matplotlib.pyplot as plt
from import_ref_data import show_eigmot_names,get_eigmot

#'Short period','Phugoid', 'initial'
name = 'Phugoid'

V_TAS = get_eigmot(name)[0]
mass = get_eigmot(name)[1] 
rho = get_eigmot(name)[2]   
pitch = get_eigmot(name)[3] #rad

alpha_0 = get_eigmot(name)[4] #rad
q_0= get_eigmot(name)[5] #rad
alpha_int = get_eigmot(name)[7]
el_int = np.array(get_eigmot(name)[8])
el_int = el_int - el_int[0]
el_int_deg = []
for i in range(len(el_int)):
    el_int_deg.append(el_int[i])
    

V_TAS_int = get_eigmot(name)[9]
pitch_int = get_eigmot(name)[10]
q_int = get_eigmot(name)[11]



def Sym_SS():
    
    W = mass*g
    
    CX0 = W * sin(pitch) / (0.5 * rho * V_TAS ** 2 * S)
    muc =  mass / (rho * S * c)
    CZ0 = -W * cos(pitch) / (0.5 * rho * V_TAS ** 2 * S)
    print(CX0)
    print(muc)
    print(CZ0)
    print(W)
    # Vector with dimensions
    C1 = np.matrix([[-2*muc*(c/V_TAS**2), 0.,0.,0.],
                     [0., (CZadot - 2*muc)*(c/V_TAS), 0., 0.],
                     [0.,0.,-(c/V_TAS), 0.],
                     [0., Cmadot*(c/V_TAS), 0., -2*muc*KY2*(c/V_TAS)**2]])

    C2 = np.matrix([[CXu*(1/V_TAS), CXa, CZ0, CXq*(c/V_TAS)],
                    [CZu*(1/V_TAS), CZa, -CX0, (CZq + 2*muc)*(c/V_TAS)],
                    [0.,0.,0.,1*(c/V_TAS)],
                    [Cmu*(1/V_TAS), Cma, 0., Cmq*(c/V_TAS)]])
    
    C3 = np.matrix([[CXde],
                    [CZde],
                    [0.],
                    [Cmde]])
    
    # Dimensionless vector
    C11 = np.matrix([[-2*muc, 0.,0.,0.],
                     [0., (CZadot - 2*muc), 0., 0.],
                     [0.,0.,-1, 0.],
                     [0., Cmadot, 0., -2*muc*KY2]])

    C22 = np.matrix([[CXu, CXa, CZ0, CXq],
                    [CZu, CZa, -CX0, (CZq + 2*muc)],
                    [0.,0.,0.,1.],
                    [Cmu, Cma, 0., Cmq]])
    
    C33 = np.matrix([[CXde],
                    [CZde],
                    [0.],
                    [Cmde]])
    
    
    Cs = np.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])
    
    Ds = np.matrix([[0.],[0.],[0.],[0.]])
    
    As = np.dot(-np.linalg.inv(C1),C2)
    Bs = np.dot(-np.linalg.inv(C1),C3)
    sys = control.ss(As,Bs,Cs,Ds)
    #print(sys)
    
    Ass = np.dot(-np.linalg.inv(C11),C22)
    Bss = np.dot(-np.linalg.inv(C11),C33)
    sys2 = control.ss(Ass,Bss,Cs,Ds)
    
    eigs = np.linalg.eig(sys.A)
    eigs2 = np.linalg.eig(sys2.A)

   # print(V_TAS)
   # print(c)
    
    print("Eigenvalues with dimension", eigs[0])
    print("Dimensionless eigenvectors", eigs2[0])
    
    realpart = eigs2[0].real
    imagpart = eigs2[0].imag
    Period=[]
    HalfT = []
    Dampratio = []
    
    for i in range(len(realpart)):
        P= ((2*pi)/(imagpart[i]))*(c/V_TAS)
        Period.append(P)
        Thalf= (log(1/2)/realpart[i])*(c/V_TAS)
        HalfT.append(Thalf)
        Damp = -realpart[i]/(realpart[i]**2 + imagpart[i]**2)**0.5
        Dampratio.append(Damp)
    print("Period=",Period)
    print("Thalf", HalfT)
    print("Dampratio",Dampratio)
    
    initial = True 
    
    if initial == True:
        
        u = 0#100
        a = radians(2)
        the = 0#0.04
        q = 0#.04
        
        X0 = np.array([u, a ,the , q])
        t1 = np.arange(0, 150, 0.1)
        y1,t1 = control.initial(sys, t1, X0)
        
        #print(y1)
        
        y_alpha_1=[]
        y_theta_1 = []
        y_q_1 = []
        y_V_1 = []
        
        for i in range(len(y1)):
            y_alpha_1.append(degrees(y1[i][1]))
            y_theta_1.append(degrees(y1[i][2]))
            y_q_1.append(degrees(y1[i][3]))
            y_V_1.append(y1[i][0]/cos(radians(y1[i][1])))
          
        # Plots for the short period motion
        
        plt.subplot(4,1,1)
        plt.plot(t1,y_V_1,'b-')
        plt.title('Speed', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('V [m/sec]')
        
        plt.subplot(4,1,2)
        plt.plot(t1,y_alpha_1,'b-')
        plt.title('Angle of attack', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('\u03B1 [deg]')
        
        plt.subplot(4,1,3)
        plt.plot(t1,y_theta_1,'b-')
        plt.title('Pitch angle', fontweight="bold")
        plt.xlabel('t[sec]')
        plt.ylabel('\u03B8 [deg]')
    
        plt.subplot(4,1,4)
        plt.plot(t1,y_q_1,'b-')
        plt.title('Pitch rate', fontweight="bold")
        plt.xlabel('t [sec]')
        plt.ylabel('q [deg/sec]') 
        
        plt.show()
    
    elif initial==False:
        
        if name=='Short period':
            
            t1 = np.arange(0, 10, 0.1)
            y1,t1,x1 = control.lsim(sys, el_int, t1)
            
            # Defining arrays of the different state variables for the short period motion
            y_ed_1 = []
            y_alpha_1=[]
            y_theta_1 = []
            y_q_1 = []
            y_V_1 = []
            
            for i in range(len(y1)):
                y_ed_1.append(el_int_deg[i])
                y_alpha_1.append(degrees(y1[i][1]) + degrees(alpha_0))
                y_theta_1.append(degrees(y1[i][2]) + degrees(pitch))
                y_q_1.append(degrees(y1[i][3]) + degrees(q_0))
                y_V_1.append((y1[i][0]/cos(radians(alpha_int[i]))+ V_TAS))
              
            # Plots for the short period motion
            plt.subplot(5,1,1)
            plt.plot(t1,y_ed_1,'b-')
            plt.plot(t1,el_int_deg,'r--')
            plt.title('Elevator deflection')
            plt.xlabel('t [sec]')
            plt.ylabel('\u03B4 [Rad]')
            
            plt.subplot(5,1,2)
            plt.plot(t1,y_V_1,'b-')
            plt.plot(t1,V_TAS_int,'r--')
            plt.title('Speed', fontweight="bold")
            plt.xlabel('t [sec]')
            plt.ylabel('V [m/sec]')
            
            plt.subplot(5,1,3)
            plt.plot(t1,y_alpha_1,'b-')
            plt.plot(t1,alpha_int,'r--')
            plt.title('Angle of attack', fontweight="bold")
            plt.xlabel('t [sec]')
            plt.ylabel('\u03B1 [deg]')
            
            plt.subplot(5,1,4)
            plt.plot(t1,y_theta_1,'b-')
            plt.plot(t1,pitch_int,'r--')
            plt.title('Pitch angle', fontweight="bold")
            plt.xlabel('t[sec]')
            plt.ylabel('\u03B8 [deg]')
        
            plt.subplot(5,1,5)
            plt.plot(t1,y_q_1,'b-')
            plt.plot(t1,q_int,'r--')
            plt.title('Pitch rate', fontweight="bold")
            plt.xlabel('t [sec]')
            plt.ylabel('q [deg/sec]') 
            
            plt.show()
                
        elif name == 'Phugoid':
            
            t2 = np.arange(0, 150, 0.1)    
            y2,t2,x2 = control.lsim(sys, el_int, t2)
    
            # Defining arrays of the different state variable for the phugoid motion    
            y_ed_2 = []
            y_alpha_2=[]
            y_theta_2 = []
            y_q_2 = []
            y_V_2 = []
       
            for i in range(len(y2)):
                y_ed_2.append(el_int_deg[i])
                y_alpha_2.append(degrees(y2[i][1]) + degrees(alpha_0))
                y_theta_2.append(degrees(y2[i][2]) + degrees(pitch))
                y_q_2.append(degrees(y2[i][3]) + degrees(q_0))
                y_V_2.append(y2[i][0]/cos(radians(alpha_int[i]))+ V_TAS)
    
            # Plots for the phugoid
            plt.subplot(5,1,1)
            plt.plot(t2,y_ed_2,'b-')
            plt.plot(t2,el_int_deg,'r--')
            plt.title('Elevator deflection')
            plt.xlabel('t [sec]')
            plt.ylabel('\u03B4 [Rad]')
            
            plt.subplot(5,1,2)
            plt.plot(t2,y_V_2,'b-')
            plt.plot(t2,V_TAS_int,'r--')
            plt.title('Speed', fontweight="bold")
            plt.xlabel('t [sec]')
            plt.ylabel('V [m/sec]')
            
            plt.subplot(5,1,3)
            plt.plot(t2,y_alpha_2,'b-')
            plt.plot(t2,alpha_int,'r--')
            plt.title('Angle of attack', fontweight="bold")
            plt.xlabel('t [sec]')
            plt.ylabel('\u03B1 [deg]')
            
            plt.subplot(5,1,4)
            plt.plot(t2,y_theta_2,'b-')
            plt.plot(t2,pitch_int,'r--')
            plt.title('Pitch angle', fontweight="bold")
            plt.xlabel('t[sec]')
            plt.ylabel('\u03B8 [deg]')
        
            plt.subplot(5,1,5)
            plt.plot(t2,y_q_2,'b-')
            plt.plot(t2,q_int,'r--')
            plt.title('Pitch rate', fontweight="bold")
            plt.xlabel('t [sec]')
            plt.ylabel('q [deg/sec]') 
            plt.show()

    return muc, CZ0, CX0

Symul = Sym_SS()