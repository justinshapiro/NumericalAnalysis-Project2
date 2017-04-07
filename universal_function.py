import math


def f(x, _str):
    x = float(x)
    _str = _str.replace("e^", "math.exp")
    _str = _str.replace('^', "**")
    _str = _str.replace("sin", "math.sin")
    _str = _str.replace("cos", "math.cos")
    _str = _str.replace("tan", "math.tan")
    _str = _str.replace("log", "math.log10")
    if "ln" in _str:
        idx = _str.find("ln")
        while _str[idx] != ')':
            idx += 1
        _str = _str[:idx] + ",2" + _str[idx:]
        _str = _str.replace("ln", "math.log")
    if '!' in _str:
        x = int(x)
        idx = _str.find('!')
        if _str[idx - 1] == ')':
            while _str[idx] != '(':
                idx -= 1
        _str = _str.replace('!', "")
        _str = _str[:idx - 1] + "math.factorial(" + _str[idx - 1] + ")" + _str[idx:]

    i = 1
    while i < len(_str):
        if _str[i] == "x":
            if _str[i - 1].isdigit():
                _str = _str[:i] + "*" + _str[i:]
        i += 1

    return eval(_str)

