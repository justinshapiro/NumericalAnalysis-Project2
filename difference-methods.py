"""
Numerical Differences
Centered Differences Formula
Forward Differences
Backward Differences 
Computation of relative errors

"""


import numpy as np
import matplotlib.pyplot as plt


def function(x):
    """ define function to be differentiated """
    f = x * np.exp(x)  # only testing
    return f


def analytic(x):
    """ derivative"""
    f = (1 + x) * np.exp(x)
    return f


def forward(x, h):
    f = (function(x + h) - function(x)) / h
    return f


def backward(x, h):
    f = (function(x) - function(x - h)) / h
    return f


def central(x, h):
    f = (function(x + h) - function(x - h)) / (2 * h)
    return f


plt.figure(1)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('test function f(x) = x exp(x)')
x = np.arange(0, 1.5, 0.01);
plt.plot(x, function(x))
plt.show()

plt.figure(2)
plt.xlabel('x')
plt.ylabel('derivative df/dx')
plt.title('analytical result: plot of the derivative df/dx')
plt.plot(x, analytic(x))
plt.show()

print "forward:", forward(1, 0.01), "\n", "backward:", backward(1, 0.01), "\n", "central:", central(1,
                                                                                                    0.01), "\n", "analytic: ", analytic(
    1)

x = np.arange(0.001, 0.1, 0.001);

plt.figure(3)
plt.xlabel('step size h')
plt.ylabel('derivative')
plt.title('results for three different numerical differention schemes for derivative evaluated at x=1')
plt.plot((0, 0.12), (analytic(1), analytic(1)), 'k-')
plt.plot(x, forward(1, x), label='forward')
plt.plot(x, backward(1, x), label='backward')
plt.plot(x, central(1, x), label='central')
plt.legend(loc=0)
plt.show()


def error_forward(y):
    f = abs((forward(1, y) - analytic(1)) / analytic(1))
    return f


def error_backward(y):
    f = abs(backward(1, y) - analytic(1)) / analytic(1)
    return f


def error_central(y):
    f = abs(central(1, y) - analytic(1)) / analytic(1)
    return f


x = np.arange(0.001, 1, 0.001);

plt.figure(4)
plt.xlabel('step size h')
plt.ylabel('relative error')
plt.title('central difference method converges fastest')
plt.loglog(x, error_forward(x), label='forward')
plt.loglog(x, error_backward(x), label='backward')
plt.loglog(x, error_central(x), label='central')
plt.legend(loc=4)
plt.show()


