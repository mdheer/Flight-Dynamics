# The Kalman Filter

# Prediction step

#X : The mean state estimate of the previous step ( k −1).
#P : The state covariance of previous step ( k −1).
#A : The transition n n × matrix.
#Q : The process noise covariance matrix.
#B : The input effect matrix.
#U : The control input. 

from math import log, pi, det, exp
import numpy as np
from np.linalg import inv

def kf_predict(X, P, A, Q, B, U):
    X = np.dot(A, X) + np.dot(B, U)
    P = np.dot(A, np.dot(P, A.T)) + Q
    return(X,P) 


# Update step

#K : the Kalman Gain matrix
#IM : the Mean of predictive distribution of Y
#IS : the Covariance or predictive mean of Y
#LH : the Predictive probability (likelihood) of measurement which is computed using the Python function gauss_pdf.

def kf_update(X, P, Y, H, R):
    IM = np.dot(H, X)
    IS = R + np.dot(H, np.dot(P, H.T))
    K = np.dot(P, np.dot(H.T, inv(IS)))
    X = X + np.dot(K, (Y-IM))
    P = P - np.dot(K, np.dot(IS, K.T))
    LH = gauss_pdf(Y, IM, IS)
    return (X,P,K,IM,IS,LH)

def gauss_pdf(X, M, S):
    if M.shape()[1] == 1:
        DX = X - np.tile(M, X.shape()[1])
        E = 0.5 * np.sum(DX * (np.dot(inv(S), DX)), axis=0)
        E = E + 0.5 * M.shape()[0] * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    elif X.shape()[1] == 1:
        DX = np.tile(X, M.shape()[1])- M
        E = 0.5 * np.sum(DX * (np.dot(inv(S), DX)), axis=0)
        E = E + 0.5 * M.shape()[0] * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    else:
        DX = X-M
        E = 0.5 * np.dot(DX.T, np.dot(inv(S), DX))
        E = E + 0.5 * M.shape()[0] * log(2 * pi) + 0.5 * log(det(S))
        P = exp(-E)
    return (P[0],E[0])















