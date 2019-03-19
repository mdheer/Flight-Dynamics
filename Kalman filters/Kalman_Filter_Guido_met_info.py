# -*- coding: utf-8 -*-
"""
Created on Wed Jun 06 18:48:32 2018

Simple Kalman filter for height data set obtained with a Bebop 2 drone in the Cyberzoo.

@author: Guido de Croon
"""

import csv
import matplotlib.pyplot as plt
import numpy as np


# read the data from the csv file
z = [];
baro = [];
sonar = [];

with open('with_column_headings.csv') as csvfile:
    reader = csv.DictReader(csvfile);
    for r in reader:
        z.append(r['pos_z']);
        baro.append(r['baro_scale_down']);
        sonar.append(r['sonar']);

z = np.asarray(z).astype('float')
baro = np.asarray(baro).astype('float');
sonar = np.asarray(sonar).astype('float');

# scaling of the ground-truth height and sonar
z_optitrack = z / 100.0 + 0.02; # formula taken from the group  # 0.02 = standaard afwijking 
                                                                # gedeeld door 100 om van cm naar m te gaan
# determine all relevant variables in an interval with good values for both sensors:
good_interval = [13000, 17000];    # Interval waar er geen rare dingen gebeuren

# first deal with any constant offsets:
# Hoogte - meeting
offset_sonar = np.mean(z_optitrack[good_interval[0]:good_interval[1]] - sonar[good_interval[0]:good_interval[1]]);
# berekent de gemiddelde offset(van hoever de sonar naast de goede waarde(waarde van de optitrack) zit)
sonar +=  offset_sonar; 
# sonar + offset = goede sonar
offset_baro = np.mean(z_optitrack[good_interval[0]:good_interval[1]] - baro[good_interval[0]:good_interval[1]]);
# zelfde voor baro
baro +=  offset_baro; 
# zelfde voor baro

# Potentially would be better to use a different interval for determining the variances, or even multiple intervals:
# good_interval = [24000, 27000];

# then estimate the variance in that area:
#Variance tussen hoogte en meeting
var_baro = np.var(z_optitrack[good_interval[0]:good_interval[1]] - baro[good_interval[0]:good_interval[1]]);
var_sonar = np.var(z_optitrack[good_interval[0]:good_interval[1]] - sonar[good_interval[0]:good_interval[1]]);
# berekent variance tussen optitrack en sensors

#print(var_baro)

# plotting the signals
plt.figure();
plt.plot(z_optitrack);
plt.plot(baro);
plt.plot(sonar);
plt.legend(('z', 'baro', 'sonar'))
plt.title('Height and raw signals')
plt.xlabel('Time step [-]')
plt.ylabel('Height [m]')

# naive Kalman filter:
# Refer to https://en.wikipedia.org/wiki/Kalman_filter for the notation

# We make a system with z and vz (although not measured)

# state vector, z, vz:    
x = np.zeros([2,1]); # matrix van 2 x 1
x[0] = sonar[0]; # bovenste plek van de matrix is sonar
x[1] = 0.0; # onderste plek is 0

# state transition matrix:
F = np.zeros([2,2]); # 2 x 2 matrix
F[0, 0] = 1; 
F[0, 1] = 1;
F[1, 1] = 1;
# F[1, 0] = 0

# Covariance of the process noise:
Q = np.eye(2) * 0.1;  # identity matrix vermenigvuldigen met 0.1 

# Covariance of the observation noise:
R = np.eye(2); 
R[0,0] = var_sonar; # variance sonar
R[1,1] = var_baro;  # variance baro

# Error covariance matrix:
P = np.eye(2); # error van de estimation

# Observation model: both measurements directly measure the height:
H = np.zeros([2,2]); # matrix met sonar en baro
H[0,0] = 1;  # sonar activeren
H[1,0] = 1;  # baro activeren

# vector that will store the observations each time step:
z = np.zeros([2,1]);

# identity matrix:
I = np.eye(2);

n_steps = len(z_optitrack);
z_KF = np.asarray([0.0] * n_steps);  # matrix met de number of steps als lengte voor de position
vz_KF = np.asarray([0.0] * n_steps); # matrix met de number of steps als lengte voor de velocity

# extra options:
SOLVE_BAD_BARO = True;  # na een bepaalde hoogte werkt de baro niet meer
SOLVE_BAD_SONAR = True; # na een bepaalde hoogte werkt de sonar niet meer
bad_sonar_threshold = 1.0;

k = []
# Run the Kalman filter:
for t in range(n_steps):

    # predict:
    x_pred = np.dot(F, x); # state transition x de vorige position
    P_pred = np.dot(F, np.dot(P, np.transpose(F))) + Q; # +Q voor de noise, om de P matrix te updaten
    
    # observations of this time step:
    z[0] = sonar[t];
    z[1] = baro[t];
    
    # if the baro measures below 0 meters, don't trust it:
    if(SOLVE_BAD_SONAR and baro[t] > 0):
        z[1] = 0.0;
    
    # if the baro and sonar are very different, don't trust the sonar:
    if(SOLVE_BAD_SONAR and np.abs(sonar[t] - baro[t]) >= bad_sonar_threshold):
        R[0,0] = 1000.0; # Verhoogt de variance zeer als de sonar niet te vertrouwen is
    else:
        R[0,0] = var_sonar;
        
    # innovation:
    y = z - np.dot(H, x_pred); # the difference between what you observe and what you expect to observe(verschil tussen prediction en observation)    
    S = R + np.dot(H, np.dot(P_pred, np.transpose(H))); 
    #P_pred is prediction state
    
    # optimal Kalman gain:
    K = np.dot(P_pred, np.dot(np.transpose(H), np.linalg.inv(S)));
    k.append(K)
    
    # a posteriori estimates:
    x = x_pred + np.dot(K, y); # berekent de position
    IKH = I - np.dot(K, H); # identity matrix - kalman gain x de variances van de baro en sonar
    P = np.dot(IKH, np.dot(P_pred, np.transpose(IKH))) + np.dot(K, np.dot(R, np.transpose(K))); # State covariance matrix(error in de estimate)

    # store the state for visualization:
    z_KF[t] = x[0]; 
    vz_KF[t] = x[1];

# output of Kalman filter:
plt.figure();
plt.plot(z_optitrack);
plt.plot(z_KF);
plt.legend(('z', 'filter'))
