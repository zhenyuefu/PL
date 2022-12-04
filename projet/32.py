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
        n = len(w)  # nombre d'objectif
        p = len(c)  # nombre de projet
        w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
        w_prime.append(w[n - 1])

        # ajout des variables
        x = MODEL.addVars(p, vtype=GRB.BINARY, name="x")  # projet auquel on attribue le budget
        r = MODEL.addVars(n, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
        b = MODEL.addVars(n, n, vtype=GRB.CONTINUOUS, lb=0, name="b")
        z = [sum(u[i][j] * x[j] for j in range(p)) for i in range(n)]

        # ajout des contraintes
        MODEL.update()
        MODEL.addConstrs((x[i] <= 1 for i in range(p)))  # contrainte x <= 1
        MODEL.addConstr((gp.quicksum(c[i] * x[i] for i in range(p)) <= budget))  # contrainte de budget
        MODEL.addConstrs((r[k] - b[i, k] <= z[i] for i in range(n) for k in range(n)))

        # ajout de la fonction objectif
        MODEL.setObjective(
            gp.quicksum(w_prime[k] * ((k + 1) * r[k] - gp.quicksum(b[i, k] for i in range(n))) for k in range(n)),
            GRB.MAXIMIZE)
        MODEL.optimize()

        return MODEL.Runtime

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


avg_runtime_n = []
runtime_p = {i: [] for i in [5, 10, 15, 20, 50, 75, 100]}
for n in (2, 5, 10, 20, 30):
    avg_runtime = []
    for p in (5, 10, 15, 20, 50, 75, 100):
        runtime = []
        for i in range(10):
            c = np.random.randint(0, 100, p)
            b = c.sum() / 2
            w = random.sample(range(1, 3 * n), n)
            w.sort(reverse=True)
            u = np.random.randint(0, 100, size=(n, p))  # random matrix of size n x p
            time = selection_multicritere_projet(c, b, w, u)
            runtime.append(time)
        # output the average runtime to a file
        avg_runtime.append(np.mean(runtime))
        runtime_p[p].append(np.mean(runtime))
        with open("32mat.txt", "a") as f:
            f.write(f"n = {n}, p = {p}, runtime = {np.mean(runtime)}\n")
    avg_runtime_n.append(np.mean(avg_runtime))
f.close()
avg_runtime_p = [np.mean(runtime_p[i]) for i in runtime_p]

# plot the result
import matplotlib.pyplot as plt

n = [2, 5, 10, 20, 30]
plt.plot(n, avg_runtime_n)
plt.xlabel("n")
plt.ylabel("average runtime")
plt.title("average runtime according to n")
# save as svg
plt.savefig("32_n.png")
plt.show()
ratio_n = np.mean([(avg_runtime_n[i] - avg_runtime_n[i - 1]) / (n[i] - n[i - 1]) for i in range(1, len(n))])

p = [5, 10, 15, 20, 50, 75, 100]
print(avg_runtime_p)
plt.plot(p, avg_runtime_p)
plt.xlabel("p")
plt.ylabel("average runtime")
plt.title("average runtime of according to p")
# save as svg
plt.savefig("32_p.png")
plt.show()

ratio_p = np.mean([(avg_runtime_p[i] - avg_runtime_p[i - 1]) / (p[i] - p[i - 1]) for i in range(1, len(p))])
print(ratio_n)
print(ratio_p)
