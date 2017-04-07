
"""
To calculate the QR Factorization of a matrix A
with NumPy/SciPy, used  the built-in
linalg library via the linalg.qr function.

"""

import pprint
import scipy
import scipy.linalg   # SciPy Linear Algebra Library

   A = scipy.array([[1, -4], [2,3], [2,2]])  # test values
   Q, R = scipy.linalg.qr(A)
   
   print "A:"
   pprint.pprint(A)
   
   print "Q:"
   pprint.pprint(Q)
   
   print "R:"          # R must be an upper triangular matrix
   pprint.pprint(R)

   
   
   
