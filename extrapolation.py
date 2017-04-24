from __future__ import print_function
import numpy
from universal_function import f

def richardson(_fstr, x, n, h):
    d = numpy.array([[0] * (n + 1)] * (n + 1), float)
    for i in xrange(n + 1):
        d[i, 0] = 0.5 * (f(x + h, _fstr) - f(x - h, _fstr)) / h
        powerOf4 = 1
        for j in xrange(1, i + 1):
            powerOf4 = 4 * powerOf4
            d[i, j] = d[i, j - 1] + (d[i, j - 1] - d[i - 1, j - 1]) / (powerOf4 - 1)
        h = 0.5 * h
    return d[n, n]

n = 1
x = 2
h = 0.01
_fstr = "1/x"
Q = richardson(_fstr, x, n, h)
print(Q)
