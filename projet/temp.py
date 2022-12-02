import gurobipy as gp
import numpy as np
from gurobipy import GRB

from projet.utils import print_solution


def partage_equitable(n, p, w, u):
    try:
        MODEL = gp.Model("22")
        w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
        w_prime.append(w[n - 1])
        index = range(n)
        xj = range(p)
        x = MODEL.addMVar((n, p), vtype=GRB.BINARY, name="x")
        r = MODEL.addVars(index, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
        b = MODEL.addVars(index, index, vtype=GRB.CONTINUOUS, lb=0, name="b")
        z = MODEL.addMVar(n, vtype=GRB.CONTINUOUS, name="z")
        MODEL.update()
        MODEL.addConstrs((gp.quicksum(x[i, j] for i in index) <= 1 for j in xj), "x")
        MODEL.addConstr(z == (u * x).sum(axis=1))
        MODEL.addConstrs((r[i] - b[i, j] <= z[j] for i in index for j in index))
        MODEL.setObjective(gp.quicksum(w_prime[k] * (k * r[k] - gp.quicksum(b[i, k] for i in index)) for k in index),
                           GRB.MAXIMIZE)
        MODEL.optimize()
        print_solution(MODEL)

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

# generate random matrix u of size n x p
n = 3
p = 6
# generate random vector w of size n in order decreasing
w = [3, 2, 1]
u = np.random.randint(0, 100, size=(n, p))     # random matrix of size n x p

for n in (5,10,15,20):
    p = 5 * n
    partage_equitable(n, p , [3, 2, 1], np.array([[325, 225, 210, 115, 75, 50]]))

