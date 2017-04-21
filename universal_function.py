import math
import numpy as np


def f(x, _str, y="null"):
    # convert x to float as required
    x = float(x)
    if y != "null":
        y = float(y)

    # no capital letters in function
    _str = _str.lower()

    # no spaces
    _str = _str.replace(' ', "")

    # convert expressions of the form a^b to a**(b)
    i = 0
    while i + 1 < len(_str):
        if _str[i] == '^' and _str[i + 1] != '(':
            _str = _str[:i + 1] + "(" + _str[i + 1:]
            i += 2
            if i >= len(_str):
                _str += ")"
            else:
                while i < len(_str) and (_str[i].isdigit() or _str[i] == "x"):
                    i += 1
                _str = _str[:i] + ")" + _str[i:]
        i += 1
    _str = _str.replace("e^", "math.exp")
    _str = _str.replace('^', "**")

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
    if "ln" in _str:
        idx = _str.find("ln")
        while _str[idx] != ')':
            idx += 1
        _str = _str[:idx] + ",2" + _str[idx:]
        _str = _str.replace("ln", "math.log")

    # handle factorial expressions
    if '!' in _str:
        x = int(x)
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

    # convert multiplication of the form ax to a*x
    i = 1
    while i < len(_str):
        if _str[i] == "x":
            if _str[i - 1].isdigit():
                _str = _str[:i] + "*" + _str[i:]
        i += 1

    result = ""
    try:
        result = float(eval(_str))
    except (TypeError, SyntaxError, NameError):
        print("Error: Incorrect syntax, please see manual for proper syntax.")
        result = "err"

    return result
