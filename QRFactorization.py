
#Linear Least Squares

"""
To calculate the QR Factorization of a matrix A to 
solve the least squares problem
with NumPy/SciPy. 
Used  the built-in linalg library via 
the linalg.qr function.

"""

import pprint
import scipy
import scipy.linalg   # SciPy Linear Algebra Library

   A = scipy.array([[1, -4], [2,3], [2,2]])  # test values, also tested 3 by 3
   Q, R = scipy.linalg.qr(A)
   
   print "A:"
   pprint.pprint(A)
   
   print "Q:"
   pprint.pprint(Q)
   
   print "R:"          # R must be an upper triangular matrix
   pprint.pprint(R)

   
   
   
