import numpy as np
from universal_function import *
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


def trap_error(_fstr, a, b):
    _fstr = format(1, _fstr, ['x'])
    _fstr = parse_expr(_fstr)
    _fstr = str(diff(diff(_fstr)))
    c = (b + a) / float(2)
    h = b - a
    result = abs(((h**3) / float(12)) * f(c, _fstr))
    return result


def simp_error(_fstr, a, b):
    _fstr = format(1, _fstr, ['x'])
    _fstr = parse_expr(_fstr)
    _fstr = str(diff(diff(diff(diff(_fstr)))))
    c = (b + a) / float(2)
    h = b - a
    result = abs(((h**5) / 90) * (f(c, _fstr)))
    return result


def trapezoid(fstr, a, b, n):
    # get intervals
    h = (b - a) / float(n)
    x = np.arange(a, b + h, h)
    # sum intervals
    trap = f(x[0], fstr) + f(x[n], fstr)
    for i in range(1, n):
        trap += 2 * f(x[i], fstr)
    trap = (h / float(2.0)) * trap
    return trap


# -------------------------------------
# simpson
# -------------------------------------
def simpson(fstr, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / float(n)
    x = np.arange(a, b + h, h)
    # sum intervals
    simp = f(x[0], fstr) + f(x[n], fstr)
    for i in range(1, n):
        if i % 2 == 0:
            w = 2
        else:
            w = 4
        simp += w * f(x[i], fstr)
    simp = (h / 3.0) * simp
    return simp

# romberg method
 # -------------------------------------
def romberg(fstr ,a, b, n):
    # initialize romberg matrix
    steps = []
    R      = np.zeros((n,n))
    R[0,0] = 0.5*(b-a)*(f(a, fstr)+f(b, fstr))
    # fill first column of romberg matrix
    for i in range(1,n):
        pts  = 2**i
        h    = (b-a)/float(pts)
        steps.append(h)
        psum = 0
        for j in range(1, pts):
            if j % 2 != 0:
                psum += f(a + j*h, fstr)
        # populate matrix
        R[i,0] = 0.5*R[i-1,0] + h*psum
    # get integral from romberg matrix
    for i in range(1,n):
        for j in range(i,n):
            r1 = R[j,i-1]
            r0 = R[j-1,i-1]
            k  = 1.0/ float((4.0**i-1))
            R[j,i] = r1 + k*(r1 - r0)
    romb = R[n-1,n-1]
    return romb
