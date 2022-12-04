import random

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def partage_equitable(n, p, w, u):
    try:
        MODEL = gp.Model("22")
        print(f"w = {w}")
        print(f"u = {u}")
        w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
        w_prime.append(w[n - 1])
        w_prime = np.array(w_prime)
        print(f"w' = {w_prime}")
        x = MODEL.addMVar((n, p), vtype=GRB.BINARY, name="x")
        r = MODEL.addMVar(n, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
        b = MODEL.addMVar((n, n), vtype=GRB.CONTINUOUS, lb=0, name="b")
        k = np.arange(1, n + 1)
        # z_i = sum(u_i,j * x_i,j)
        z = np.array([u[i, :] @ x[i, :] for i in range(n)])
        MODEL.update()

        # x的每一列的和不超过1
        MODEL.addConstr(x.sum(axis=0) <= 1, "x")
        # r_k - b_i,k - z_i <= 0
        for k in range(n):
            for i in range(n):
                MODEL.addConstr(r[k] - b[i, k] - z[i] <= 0, "r")
        MODEL.setObjective(sum(w_prime * (r * k - b.sum(axis=0))), GRB.MAXIMIZE)
        MODEL.optimize()
        # print_solution(MODEL)
        if MODEL.status == GRB.OPTIMAL:
            print("solution:")
            for i in range(n):
                print(f"z{i} = {z[i].getValue()}")
            print()
            for i in range(n):
                for j in range(p):
                    if x[i, j].x > 0:
                        print(f"x{i}_{j} = {x[i, j].x}", end=" ")
                print()
            print("objective value = ", MODEL.objVal)
        else:
            print("No solution")
        # print solution time
        print("solution time = ", MODEL.Runtime, "s")

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    # except AttributeError:
    #     print('Encountered an attribute error')
    return MODEL.Runtime


avg_runtime = []
for n in (5, 10, 15, 20, 25):
    p = 5 * n
    runtime = []
    for i in range(10):
        w = random.sample(range(1, 3 * n), n)
        w.sort(reverse=True)
        u = np.random.randint(0, 100, size=(n, p))  # random matrix of size n x p
        time = partage_equitable(n, p, w, u)
        runtime.append(time)
    # output the average runtime to a file
    avg_runtime.append(np.mean(runtime))
    with open("22.txt", "a") as f:
        f.write(f"n = {n}, p = {p}, runtime = {np.mean(runtime)}\n")
f.close()

# plot the result
import matplotlib.pyplot as plt

n = [5, 10, 15, 20, 25]
plt.plot(n, avg_runtime)
plt.xlabel("n")
plt.ylabel("average runtime")
plt.title("average runtime of partage_equitable")
# save as svg
plt.savefig("22.svg")
plt.show()

# Test case
# n = 3
# p = 6
# w = [3, 2, 1]
# u = np.array([[325, 225, 210, 115, 75, 50]])
# u = np.repeat(u, 3, axis=0)
# partage_equitable(n, p, w, u)
