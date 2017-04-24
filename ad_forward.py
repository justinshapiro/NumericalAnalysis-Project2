'''
    Implements Forward Automatic Differentiation
    ADForwardFloat class found at http://blog.tombowles.me.uk/2014/09/10/ad-algorithmicautomatic-differentiation/
    Using this ADForwardFloat class that provides some "overloading" of operators we can implement forward AD

'''


from universal_function import format
import ad
from ad.admath import *
import math

class ADForwardFloat(object):
    def __init__(self, val, delta):
        # The "actual" value (black square)
        self.val = val
        # The corresponding increment
        self.delta = delta

    def __add__(self, other):
        if type(other) is int or type(other) is float:
            other_conv = ADForwardFloat(float(other), 0,0)
        # If F(x,y) = x + y, then J_F,x,y(delta_x, delta_y) = delta_y + delta_x
        print str(self.val) + ' + ' + str(other_conv.val)
        return ADForwardFloat(self.val + other_conv.val, other_conv.delta + self.delta)

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            other_conv = ADForwardFloat(float(other), 0,0)
        # If F(x,y) = x * y, then J_f,x,y(delta_x, delta_y) = y*delta_x + x*delta_y
        return ADForwardFloat(self.val * other_conv.val, other_conv.val * self.delta + self.val * other_conv.delta)

    def __div__(self, other):
        if type(other) is int or type(other) is float:
            other_conv = ADForwardFloat(float(other), 0,0)
        # If F(x,y) = x / y, then J_f,x,y(delta_x, delta_y) = (delta_x - (x / y) * delta_y) / y
        return ADForwardFloat(self.val / other_conv.val, (self.delta - (self.val / other_conv.val) * other_conv.delta) / other_conv.val)

class forwardAutoDiff(object):
    def __init__(self, f, g, x):
        self.f = f
        self.f = self.f.replace('math', 'admath')
        self.g = g
        self.x = ad.adnumber(x)
        self.g_x = 0
        self.g_x_prime = 0
        self.f_x = 0
        self.f_x_prime = 0

    def __int__(self, val):
        return ADForwardFloat(float(val), 0.0)

    def calcG(self):
        x = self.x
        self.g_x = eval(self.g)
        return float(self.g_x)

    def g_deriv(self):
        self.g_x_prime = self.g_x.d(self.x)
        return float(self.g_x_prime)

    def calcF(self):
        g = self.g_x
        x = self.x
        self.f_x = eval(self.f)
        return float(self.f_x)

    def f_deriv(self):
        x = self.x
        self.f_x_prime = self.f_x.d(self.x)
        return float(self.f_x_prime)

# EXAMPLE
'''
g = '(3*x*x*x + 2*x*x - 5*x - 4) / (x * x + 1)'
#g = '(3*x^3 + 2*x^2-5*x-4)/(x^2+1)'
g = format(0, g, ['x'])
print g
testIn = forwardAutoDiff(format(0, 'tan(g) + x*x*x*x - 2*x*x*x', ['g']), g, float(3))

gValues = float(testIn.calcG()), float(testIn.g_deriv())

print 'x = ' + str(float(testIn.x))

print 'g(x) = ' + str(testIn.g)
print 'g(x), g\'(x) at x = ' + str(float(testIn.x)) + ': ' + str(gValues)

print 'f = ' + str(testIn.f)

result = (testIn.calcF(), testIn.f_deriv())
print 'S(f, f\') = ' + str(result)
'''
