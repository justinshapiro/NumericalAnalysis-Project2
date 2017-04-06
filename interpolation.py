from chebyshev import Chebyshev
import math


'''
Chebyshev
-------------

User provides the interval [a, b] the degree of the Chebyshev interpolating polynomial (d) and f(x)
    -> a, b, d, f(x)
Program outputs a list where list[0] = approximation and list[1] is error
    -> return_value[0] = approximation, return_value[1] = error
'''
c = Chebyshev(-1, 1, 5, math.exp)
result = c.eval(1)
error = math.exp(1) / (math.pow(2, 4) * math.factorial(5))

