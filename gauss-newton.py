#Gauss-Newton algorithm for solving nonlinear least squares problem

import scipy
import numpy as np
from numpy.linalg import inv
import math
import scipy.misc

#TEST VALUES
s = [0.038,0.194,0.425,0.626,1.253,2.500,3.740]
rate = [0.050,0.127,0.094,0.2122,0.2729,0.2665,0.3317]
iterations = 5 #taking iterations as 5
rows = 7    #taking no of rows as 7
columns = 2 #taking no of columns as 2

#This is original guess
B = np.matrix([[.9],[.2]])
print B#printing original guess B

jf = np.zeros((rows,columns)) #Jacobian matrix from below r
r = np.zeros((rows,1)) #for r equations

def model(Vmax,Km,Sval):
   return ((Vmax*Sval)/(Km+Sval))

#partial derivation for B2 and xi
def partialDerivativeB1(B2,xi):
   return round(-(xi/(B2+xi)),10)

#partial derivation for B1 and B2 and xi
def partialDerivativeB2(B1,B2,xi):
   return round(((B1*xi)/((B2+xi)*(B2+xi))),10)

def residual(x,y,B1,B2):
   return (y - ((B1*x)/(B2+x)))

for i in xrange(iterations):
   sumofResid = 0
   #calculate Jr and r for iteration
   for j in xrange(rows):
       r[j,0] = residual(S[j],rate[j],B[0],B[1])
       sumofResid += (r[j,0]*r[j,0])
       Jf[j,0] = partialDerivativeB1(B[1],S[j])
       Jf[j,1] = partialDerivativeB2(B[0],B[1],S[j])
   Jft = Jf.T
   B -= np.dot(np.dot(inv(np.dot(Jft,Jf)),Jft),r)
   print B