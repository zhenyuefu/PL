import gurobipy as gp
import numpy as np
from gurobipy import GRB

try:
    MODEL = gp.Model("14")
    n = 2
    w = [2, 1]
    w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
    w_prime.append(w[n - 1])
    index = range(n)
    xi = range(5)
    x = MODEL.addMVar(5, vtype=GRB.BINARY, name="x")
    r = MODEL.addVars(index, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
    b = MODEL.addVars(index, index, vtype=GRB.CONTINUOUS, lb=0, name="b")
    z_coefficient = np.array([[5, 6, 4, 8, 1], [3, 8, 6, 2, 5]])
    z = MODEL.addMVar(n, vtype=GRB.CONTINUOUS, name="z")
    MODEL.update()
    MODEL.addConstr(gp.quicksum(x[i] for i in xi) == 3, "x")
    MODEL.addConstr(z == z_coefficient @ x, "z")
    MODEL.addConstrs((r[i] - b[i, j] <= z[j] for i in index for j in index))
    MODEL.setObjective(gp.quicksum(w_prime[k] * (k * r[k] - gp.quicksum(b[i, k] for i in index)) for k in index),
                       GRB.MAXIMIZE)
    MODEL.optimize()
    print("solution:")
    for i in index:
        print("z[", i+1, "] = ", z[i].x)
    for i in xi:
        print("x[", i+1, "] = ", x[i].x)
    print("objective value = ", MODEL.objVal)


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
