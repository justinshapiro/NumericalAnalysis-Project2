from numpy import *

def nest(c, x, b=None):
    if b is None:
        b = []
    d = len(c) - 1
    if not b:
        b = zeros(d)
    y = c[d]
    for i in range(d - 1, -1, -1):
        y *= (x - b[i])
        y += c[i]
    return y


def newtdd(x, y):
    n = len(x)
    v = zeros((n, n))
    for j in range(n):
        v[j, 0] = y[j]
    for i in range(1, n):
        for j in range(n - i):
            v[j, i] = (v[j + 1, i - 1] - v[j, i - 1]) / (x[j + i] - x[j])
    c = v[0, :].copy()
    return c
