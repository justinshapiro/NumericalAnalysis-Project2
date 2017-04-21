from universal_function import f
import numpy as np
import math
import matplotlib.pyplot as plt

solutions = []
rmse = []

vk = [[0], [0]] # initial is set here
x = [0, 1, 0]
y = [1, 1, -1]
radii = [1, 1, 1]

iterations = 7

base_str_x = "(x xi) / sqrt((x xi)^2 + (y yi)^2)"
base_str_y = "(y yi) / sqrt((x xi)^2 + (y yi)^2)"
base_str_rk = "sqrt((x xi)^2 + (y yi)^2) Ri"

it = 0
while it < iterations:
    i = 0
    A = []
    while i < len(x):
        A.append(["", ""])
        A0_str = base_str_x.replace(" xi", "%+f" % (x[i] * -1))
        A0_str = A0_str.replace(" yi", "%+f" % (y[i] * -1))
        A[i][0] = f(vk[0][0], A0_str, vk[1][0])
        A1_str = base_str_y.replace(" xi", "%+f" % (x[i] * -1))
        A1_str = A1_str.replace(" yi", "%+f" % (y[i] * -1))
        A[i][1] = f(vk[0][0], A1_str, vk[1][0])
        i += 1

    i = 0
    rk = []
    while i < len(x):
        rk.append([""])
        r0_str = base_str_rk.replace(" xi", "%+f" % (x[i] * -1))
        r0_str = r0_str.replace(" yi", "%+f" % (y[i] * -1))
        r0_str = r0_str.replace("Ri", "%+f" % (radii[i] * -1))
        rk[i][0] = f(vk[0][0], r0_str, vk[1][0])
        i += 1

    lhs = np.matmul(map(list, zip(*A)), A)
    rhs = -1 * np.matmul(map(list, zip(*A)), rk)
    vk = np.linalg.solve(lhs, rhs)
    vk = vk.tolist()
    solutions.append(vk)
    print(vk)

    inner_square = 0
    for r in rk:
        inner_square += float(r[0]) ** 2
    rmse.append(math.sqrt(inner_square / float(len(rk))))
    it += 1

graph_x = []
i = 0
while i < iterations:
    graph_x.append(i + 1)
    i += 1

plt.plot(graph_x, rmse)
plt.xlabel("Iterations")
plt.ylabel("RMSE")
plt.title("RMSE over Iterations")
plt.show()
