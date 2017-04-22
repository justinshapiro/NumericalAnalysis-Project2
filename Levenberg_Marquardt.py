# Playing with this
'''
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from universal_function import f, format

a, b, c, x = symbols('a b c x', real=True)
# model = "ae^(-b(x-c)^2)"
# model = format(1, model, ['a', 'b', 'c', 'x'])
str_expr = "a*exp(-b*(x-c)**(2))"
parsed_expr = parse_expr(str_expr)
result = diff(parsed_expr, x)
print(result)
x_arr = [1, 2, 2, 3, 4]
y_arr = [3, 5, 7, 5, 1]
vk = [1, 1, 1]
'''