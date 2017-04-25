import math

class Chebyshev:
    def __init__(self, a, b, n, func, eval_str):
        self.a = a
        self.b = b
        self.c = []
        self.func = func
        self.err = False
        f = []

        bma = 0.5 * (b - a)
        bpa = 0.5 * (b + a)
        try:
            f = [func(math.cos(math.pi * (k + 0.5) / n) * bma + bpa, eval_str) for k in range(n)]
            fac = 2.0 / n
            self.c = [fac * sum([f[k] * math.cos(math.pi * j * (k + 0.5) / n)
                                 for k in range(n)]) for j in range(n)]
        except TypeError:
            self.err = True
            pass

    def eval(self, x):
        if not self.err:
            if x.find('.') != -1:
                x = float(x)
            else:
                x = int(x)
            a,b = self.a, self.b
            y = (2.0 * x - a - b) * (1.0 / (b - a))
            y2 = 2.0 * y
            (d, dd) = (self.c[-1], 0)             # Special case first step for efficiency
            for cj in self.c[-2:0:-1]:            # Clenshaw's recurrence
                (d, dd) = (y2 * d - dd + cj, d)
            return y * d - dd + 0.5 * self.c[0]   # Last step is different
        else:
            return "err"
