import math
import numpy as np


def format(_type, _str, var_list):
    # no capital letters in function
    _str = _str.lower()

    # no spaces
    _str = _str.replace(' ', "")

    # handle this exception if _str came from sympy
    _str = _str.replace("exp", "e^")

    # convert expressions of the form a^b to a**(b)
    i = 0
    while i + 1 < len(_str):
        if _str[i] == '^' and _str[i + 1] != '(':
            _str = _str[:i + 1] + "(" + _str[i + 1:]
            i += 2
            if i >= len(_str):
                _str += ")"
            else:
                while i < len(_str) and (_str[i].isdigit() or _str[i] in var_list):
                    i += 1
                _str = _str[:i] + ")" + _str[i:]
        i += 1

    # convert multiplication of the form ax to a*x
    no_mul_symbols = [')', '^', '*', '+', '-', '/']
    i = 0
    while i < len(_str):
        # this_str = _str[i], for debugging
        if _str[i] in var_list or _str[i].isdigit():
            if i + 1 < len(_str) and _str[i + 1] not in no_mul_symbols:
                if i > 0:
                    _str = _str[:i + 1] + "*" + _str[i + 1:]
                else:
                    _str = _str[i] + "*" + _str[i + 1:]
        i += 1

    if _type == 0:
        _str = _str.replace("exp", "math.exp")
        _str = _str.replace("e^", "math.exp")
    else:
        _str = _str.replace("e^", "exp")
    _str = _str.replace('^', "**")

    if _type == 0:
        # convert trig and log functions to their Pythonic values
        _str = _str.replace("sqrt", "math.sqrt")
        _str = _str.replace("sin", "math.sin")
        _str = _str.replace("asin", "math.asin")
        _str = _str.replace("sin**-1", "math.asin")
        _str = _str.replace("sin**(-1)", "math.asin")
        _str = _str.replace("cos", "math.cos")
        _str = _str.replace("acos", "math.acos")
        _str = _str.replace("cos**-1", "math.acos")
        _str = _str.replace("cos**(-1)", "math.acos")
        _str = _str.replace("tan", "math.tan")
        _str = _str.replace("asin", "math.asin")
        _str = _str.replace("tan**-1", "math.atan")
        _str = _str.replace("tan**(-1)", "math.atan")
        _str = _str.replace("log", "math.log10")
        _str = _str.replace("ln", "math.log")

        # handle factorial expressions
        if '!' in _str:
            idx = _str.find('!')
            if _str[idx - 1] == ')':
                paren_stack = 1
                while paren_stack > 0 and idx > 0:
                    if _str[idx] == ')':
                        paren_stack += 1
                    elif _str[idx] == '(':
                        paren_stack -= 1
                    idx -= 1
            _str = _str.replace('!', "")
            _str = _str[:idx] + "math.factorial(" + _str[idx] + ")" + _str[idx:]

    return _str


def f(x, _str, y="null", *_vars):
    var_list = ['x']
    if '!' in _str:
        x = int(x)
    else:
        x = float(x)
    if y != "null":
        y = float(y)
        var_list.append('y')

    next_var = 'a'
    i = 0
    while i < len(_vars):
        var_list.append(chr(ord(next_var) + i))
        i += 1

    _str = format(0, _str, var_list)

    try:
        result = float(eval(_str))
    except (TypeError, SyntaxError, NameError):
        result = "err"

    return result
