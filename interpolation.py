from chebyshev import Chebyshev
import bezier
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy
from scipy import interpolate

def sign_of(var):
    if var >= 0:
        return " + "
    else:
        return " "


'''
Chebyshev
-------------

User provides the interval [a, b] the degree of the Chebyshev interpolating polynomial (d) and f(x)
    -> a, b, d, f(x)
Program outputs a list where list[0] = approximation and list[1] is error
    -> return_value[0] = approximation, return_value[1] = error
'''

a = -1
b = 1
d = 5
func = math.exp
c = Chebyshev(a, b, d, func, "")

# to GUI
result = c.eval(1)

# to GUI
error = math.exp(1) / (math.pow(2, 4) * math.factorial(5))


'''
Bezier (using pip install bezier)
--------------------------------------

User provides x(t) and y(t) as strings 
Program outputs the two endpoints and two control points
Program will also generate a graph
    -> x_t and y_t (strings)
'''


x1 = 1
x2 = 1
x3 = 3
x4 = 2
y1 = 1
y2 = 3
y3 = 3
y4 = 2
bx = 3 * (x2 - x1)
by = 3 * (y2 - y1)
cx = 3 * (x3 - x2) - bx
cy = 3 * (y3 - y2) - by
dx = x4 - x1 - bx - cx
dy = y4 - y1 - by - cy
data_points_x = [x1, x2, x3, x4]
data_points_y = [y1, y2, y3, y4]
nodes = np.array([
    [x1, y1],
    [x2, y2],
    [x3, y3],
    [x4, x4],
])
curve = bezier.Curve(nodes, degree=3)
ax = curve.plot(num_pts=256)
ax.axis('scaled')
ax.set_xlim(min(data_points_x) - 0.25, max(data_points_x) + 0.25)
ax.set_ylim(min(data_points_y) - 0.25, max(data_points_y) + 0.25)
plt.show()

# to GUI
x_t = "x(t) = " + str(x1) + sign_of(bx) + \
      str(bx) + "t" + sign_of(cx) + str(cx) + \
      "t^2"  + sign_of(dx) + str(dx) + "t^3"

# to GUI
y_t = "y(t) = " + str(y1) + sign_of(by) + \
      str(by) + "t" + sign_of(cy) + str(cy) + \
      "t^2"  + sign_of(dy) + str(dy) + "t^3"


'''
Cubic splines
-------------
Input: a set of data points
Output: Spline equations S_i(x) for i = 0, ..., n - 1

How many data points?: n = user_input
Dynamically generate input boxes
Generate list of required variables: [[delta_i, Delta_i]]
'''

x = np.array([1, 2, 4, 5])
y = np.array([2, 1, 4, 3])
xx = np.arange(np.amin(x), np.amax(x) + .01, 0.01)
s1 = interpolate.InterpolatedUnivariateSpline(x, y)
s2 = interpolate.UnivariateSpline(x[::-1], y[::-1], s=0.1)
plt.plot (x, y, 'bo', label='Data')
plt.plot (xx, s2(xx), 'r-', label='Spline, fit')
plt.legend()
plt.show()

