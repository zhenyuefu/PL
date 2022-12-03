import random

import gurobipy as gp
import numpy as np
from gurobipy import GRB

def selection_multicritere_projet(c, budget, w, u):
    """
    :param c: liste des coûts des projets
    :param budget: budget a ne pas dépasser
    :param w: liste des poids des objectifs
    :param u: matrice des utilités de chaque projet pour chaque objectif
    """
    try:
        MODEL = gp.Model("31")
        n = len(w) # nombre d'objectif
        p = len(c) # nombre de projet
        w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
        w_prime.append(w[n - 1])
        index_n = range(n)
        index_p = range(p)

        # ajout des variables
        x = MODEL.addVars(p, vtype=GRB.BINARY, name="x") # projet auquel on attribue le budget
        r = MODEL.addVars(n, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
        b = MODEL.addVars(n, n, vtype=GRB.CONTINUOUS, lb=0, name="b")
        z = MODEL.addVars(n, vtype=GRB.CONTINUOUS, name="z")

        # ajout des contraintes
        MODEL.update()
        MODEL.addConstrs((x[i] <= 1 for i in index_p)) # contrainte x <= 1
        MODEL.addConstr((gp.quicksum(c[i] * x[i] for i in index_p) <= budget)) # contrainte de budget
        MODEL.addConstrs((z[i] == gp.quicksum(u[i][j] * x[j] for j in index_p) for i in index_n)) # contrainte sur les utilités
        MODEL.addConstrs((r[k] - b[i, k] <= z[i] for i in index_n for k in index_n))

        # ajout de la fonction objectif
        MODEL.setObjective(gp.quicksum(w_prime[k] * (k * r[k] - gp.quicksum(b[i, k] for i in index_n)) for k in index_n),
                        GRB.MAXIMIZE)
        MODEL.optimize()
        print("w = ", w)
        print("u = ", u)
        print("c = ", c)
        print("budget = ", budget)
        print("x = ", [x[i].x for i in index_p])
        print("z = ", [z[i].x for i in index_n])
        print("obj = ", MODEL.objVal)
        
        return MODEL

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

for n in (2, 5, 10):
    for p in (5, 10, 15, 20):
        runtime = []
        for i in range(10):
            c = np.random.randint(0, 100, p)
            b = c.sum()/2
            w = random.sample(range(1, 3 * n), n)
            w.sort(reverse=True)
            u = np.random.randint(0, 100, size=(n, p))  # random matrix of size n x p
            time = selection_multicritere_projet(c, b, w, u)
            runtime.append(time)
        # output the average runtime to a file
        with open("32mat.txt", "a") as f:
            f.write(f"n = {n}, p = {p}, runtime = {np.mean(runtime)}\n")
f.close()