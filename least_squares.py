import numpy as np
import math

A = np.array([[1, 1], [1, -1], [1, 1]])
B = np.array([2, 1, 3])
X = np.linalg.lstsq(A, B)
print(X[0]) # X
residual = B - np.matmul(A, X[0]) # Residual

inner_square = 0
for r in residual:
    inner_square += float(r)**2

rmse = math.sqrt(inner_square / len(residual))
print(rmse)