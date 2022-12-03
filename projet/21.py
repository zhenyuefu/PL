import gurobipy as gp
import numpy as np
from gurobipy import GRB

from projet.utils import print_solution

try:
    MODEL = gp.Model("21")
    n = 3
    p = 6
    w = [3, 2, 1]
    w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
    w_prime.append(w[n - 1])
    index = range(n)
    xj = range(p)
    x = MODEL.addVars(index, xj, vtype=GRB.BINARY, name="x")
    r = MODEL.addVars(index, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
    b = MODEL.addVars(index, index, vtype=GRB.CONTINUOUS, lb=0, name="b")
    u = np.array([[325, 225, 210, 115, 75, 50]])
    u = np.repeat(u, 3, axis=0)
    z = MODEL.addVars(index, vtype=GRB.CONTINUOUS, name="z")
    MODEL.update()
    MODEL.addConstrs((gp.quicksum(x[i, j] for i in index) <= 1 for j in xj), "x")
    MODEL.addConstrs((z[i] == gp.quicksum(u[i][j] * x[i, j] for j in xj) for i in index))
    MODEL.addConstrs((r[i] - b[i, j] <= z[j] for i in index for j in index))
    MODEL.setObjective(gp.quicksum(w_prime[k] * (k * r[k] - gp.quicksum(b[i, k] for i in index)) for k in index),
                       GRB.MAXIMIZE)
    MODEL.optimize()
    print_solution(MODEL)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')

try:
    MODEL = gp.Model("maximisant la satsifaction moyenne")
    z = MODEL.addVars(index, vtype=GRB.CONTINUOUS, name="z")
    x = MODEL.addVars(index, xj, vtype=GRB.BINARY, name="x")
    MODEL.update()
    MODEL.addConstrs((gp.quicksum(x[i, j] for i in index) <= 1 for j in xj), "x")
    MODEL.addConstrs((z[i] == gp.quicksum(u[i][j] * x[i, j] for j in xj) for i in index))
    MODEL.setObjective(gp.quicksum(z[i] for i in index) / n, GRB.MAXIMIZE)
    MODEL.optimize()
    print_solution(MODEL)
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
