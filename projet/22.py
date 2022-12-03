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
        z = MODEL.addMVar(n, vtype=GRB.CONTINUOUS, name="z")
        MODEL.update()
        # x的每一列的和不超过1
        MODEL.addConstr(x.sum(axis=0) <= 1, "x")
        MODEL.addConstr(z == (u * x).sum(axis=1))
        z = np.reshape(z, (n, 1))
        MODEL.addConstr((r - b) <= (z * np.ones((n, n))))
        MODEL.setObjective((w_prime * (r * np.arange(1, n + 1) - b.sum(axis=0))).sum(), GRB.MAXIMIZE)
        MODEL.optimize()
        # print_solution(MODEL)
        if MODEL.status == GRB.OPTIMAL:
            print("solution:")
            for i in range(n):
                print(f"z{i} = {z[i].x}", end=" ")
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

    except AttributeError:
        print('Encountered an attribute error')
    return MODEL.Runtime


for n in (5, 10, 15, 20):
    p = 5 * n
    runtime = []
    for i in range(10):
        w = random.sample(range(1, 3 * n), n)
        w.sort(reverse=True)
        u = np.random.randint(0, 100, size=(n, p))  # random matrix of size n x p
        time = partage_equitable(n, p, w, u)
        runtime.append(time)
    # output the average runtime to a file
    with open("22mat.txt", "a") as f:
        f.write(f"n = {n}, p = {p}, runtime = {np.mean(runtime)}\n")
f.close()

# Test case
# n = 3
# p = 6
# w = [3, 2, 1]
# u = np.array([[325, 225, 210, 115, 75, 50]])
# u = np.repeat(u, 3, axis=0)
# partage_equitable(n, p, w, u)
