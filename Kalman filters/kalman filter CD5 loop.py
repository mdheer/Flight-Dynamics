#modules import
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
from math import factorial
import scipy.optimize

#SAVITZKY GOLAY SMOOTHENER USED FOR ACCELEROMETER
def savitzky_golay(y, window_size, order, deriv=0, rate=1):    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')



#SETTINGS
SOLVE_BARO = True
SOLVE_SONAR = True
SONAR_BARO_TRESHOLD = 1.0
GOOD_INTERVAL = [13000,17000]

#import data
datafile = np.genfromtxt("data_file.txt",delimiter=",")
step = datafile[:,0]        #timestep
W = datafile[:,22]          #optitrack height 
S = datafile[:,18]          #sonar
T = datafile[:,10]          #thrust
ac = datafile[:,24]         #acceleration 
baro = datafile[:,26]       #baro scaled by Guido
press = datafile[:,19]      #pressure
optitrack= (W/100.0)+0.02   #optitrack correction

#LeastSquared Pressure to baro_scale_down 
x1 = np.array([press])
y1 = np.array(baro).T
A1 = np.vstack([np.ones(len(press)),x1]).T
scalar1 = np.linalg.lstsq(A1,y1)
presscaled= 0.085416202*press - 8628.03576      #baro scaled by Us

#Savitzky golay acceleration
a = -(savitzky_golay(ac,501,1) + 10.4)

#prediction
dt = 0.1
P = np.array([[0, 0],[0, 0]])       #prior P    
F = np.array([[1, dt],[0, 1 ]])     #transition matrix  
B = np.array([[(dt**2)/2],[dt]])    #control input transition matrix
q1 = 0.1
q2 = 0
q3 = 0
q4 = 0.1
Q = np.array([[q1,q2],[q3, q4]])    #process noise vector

#residuals & variance estimation
var_sonar= np.var(optitrack[GOOD_INTERVAL[0]:GOOD_INTERVAL[1]] - S[GOOD_INTERVAL[0]:GOOD_INTERVAL[1]])
var_baro= np.var(optitrack[GOOD_INTERVAL[0]:GOOD_INTERVAL[1]] - baro[GOOD_INTERVAL[0]:GOOD_INTERVAL[1]])

#Kalman estimation 
H = np.array([[1,0],[1,0]])
X = np.array([[0],[0]])
R = np.eye(2)
R[0,0]= var_sonar
R[1,1]= var_baro
estimate = []
z = np.zeros([2,1])

#prediction update loop
for i in range(len(W)):
    z[0] = S[i]
    z[1] = baro[i]
    X_ = np.dot(F,X) + a[i]*B
    P_ = np.dot(F, np.dot(P, np.transpose(F))) + Q
    if SOLVE_BARO and baro[i]>0:
        z[1] = 0.0            
    if SOLVE_BARO and np.abs(S[i]-baro[i]) >= 1.0 :
        R[0,0] = 1000.0;
    else:
        R[0,0] = var_sonar;
        
#correction update
    hp = np.dot(H,P_)
    ehh = np.dot(hp,H.T) + R
    uhh = np.linalg.inv(ehh)
    pht = np.dot(P_,H.T)
    K = np.dot(pht, uhh)            #kalman gain
    hx = np.dot(H,X_)
    X = X_ + np.dot(K,(z-hx))
    kh = np.dot(K,H)
    P = np.dot((np.eye(2)- kh),P_)
    estimate.append(X[0,0])


#input plot
plt.xlabel('Time step',fontsize=25)
plt.ylabel('Height',fontsize=25)
plt.title('Kalman filter input',fontsize=25)
plt.plot(step,optitrack)
plt.plot(step,baro)
plt.plot(step,S)
plt.plot(step,a)
plt.show()

#output plot
plt.xlabel('Time step',fontsize=25)
plt.ylabel('Height  [m]',fontsize=25)
plt.title('Kalman output (sonar,baro,accelerometer)',fontsize=15)
plt.plot(step,optitrack)
plt.plot(step,estimate)
plt.show()

