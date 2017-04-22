from __future__ import print_function
import numpy


def richardson(f, x, n, h):
    """
    Using def richardson to find approximate extrapolation f'(x) at a particular x 
    d = richardson (f, x, n, h):
    f: function to find the derivative 
    x:  value of x to find the derivative at 
    n: initial extrapolation 
    h: initial step size
    return d 
     
   """

    d = numpy.array([[0] * (n + 1)] * (n + 1), float)
    for i in xrange(n + 1):
        d[i, 0] = 0.5 * (f(x + h) - f(x + h)) / h
        powerOf4 = 1
        for j in xrange(1, i + 1):
            powerOf4 = 4 * powerOf4
        d[i, j] = d[i, j - 1] + (d[i, j - 1] - d[i - 1, j - 1]) / (powerOf4 - 1)

    h = 0.5 * h

    return d

