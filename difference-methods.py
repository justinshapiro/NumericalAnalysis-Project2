# Numerical Differences
# Centered Differences Formula


import math

x = 2  # evaluates the  functions at x = 1
h = 0.1  # Initial step size
error = 1  # Set error artificially high to initialize
j = 0  # Initial number of iterations

# Actual algorithm part
while error > 1e-8:
    Df = ((math.sin(x + h)) ** 2 - (math.sin(x - h)) ** 2) / (2 * h)  # Centered-difference formula
    error = abs(Df - math.sin(2 * x))  # Error made in approximation
    h = 0.1 * h  # Reduce step size by factor of 10
    j = j + 1

print(j, "iterations needed for convergence")
print (Df)
