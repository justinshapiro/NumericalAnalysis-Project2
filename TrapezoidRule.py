import numpy as np


# input parameters
# -------------------------------------------------
# input function
def f(x):
    f = x**2
    return f

# input limits of integration
a = 1
b = 0

# input number of intervals
n =2
# -------------------------------------------------

# analytical solution
def intf(a,b):
    intf = ((4*b-3)**4 - (4*a-3)**4)/16
    return intf
asol = intf(a,b)


def trapezoid(f, a, b, n):
    # get intervals
    h = (b - a) / float(n)
    x = np.arange(a, b + h, h)
    # sum intervals
    trap = f(x[0]) + f(x[n])
    for i in range(1, n):
        trap += 2 * f(x[i])
    trap = (h / 2.0) * trap
    return trap


# -------------------------------------

# simpson
# -------------------------------------
def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / float(n)
    x = np.arange(a, b + h, h)
    # sum intervals
    simp = f(x[0]) + f(x[n])
    for i in range(1, n):
        if i % 2 == 0:
            w = 2
        else:
            w = 4
        simp += w * f(x[i])
    simp = (h / 3.0) * simp
    return simp



# call integration routines
trap = trapezoid(f,a,b,n)
simp = simpson(f,a,b,n)

# get integration error
terr = (abs(asol-trap)/asol)*100
serr = (abs(asol-simp)/asol)*100

# print results

print '\nMethod            Solution    Error'
print '--------------------------------------'
print 'analytical     %12.6f   %6.3f'  % (asol,0),'%'
print 'trapezoid      %12.6f   %6.3f'  % (trap,terr),'%'
print 'simpson        %12.6f   %6.3f'  % (simp,serr),'%'
