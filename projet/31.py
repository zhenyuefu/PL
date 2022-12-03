import gurobipy as gp
import numpy as np
from gurobipy import GRB

from utils import print_solution

def selection_multicritere_projet(c, budget, w, z_coefficient, print=False):
    """
    :param c: liste des coûts des projets
    :param budget: budget a ne pas dépasser
    :param w: liste des poids des objectifs
    :param z_coefficient: matrice des utilités de chaque projet pour chaque objectif
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
        MODEL.addConstrs((z[i] == gp.quicksum(z_coefficient[i][j] * x[j] for j in index_p) for i in index_n)) # contrainte sur les utilités
        MODEL.addConstrs((r[i] - b[i, j] <= z[j] for i in index_n for j in index_n))

        # ajout de la fonction objectif
        MODEL.setObjective(gp.quicksum(w_prime[k] * (k * r[k] - gp.quicksum(b[i, k] for i in index_n)) for k in index_n),
                        GRB.MAXIMIZE)
        MODEL.optimize()

        return MODEL


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


def selection_multicritere_projet_moyenne(c, budget, z_coefficient):
    """
    :param c: liste des coûts des projets
    :param budget: budget à ne pas dépasser
    :param z_coefficient: matrice des utilités de chaque projet pour chaque objectif
    """
    try:
        MODEL = gp.Model("31")
        n = len(z_coefficient) # nombre d'objectif
        p = len(c) # nombre de projet
        index_n = range(n)
        index_p = range(p)

        # ajout des variables
        x = MODEL.addVars(p, vtype=GRB.BINARY, name="x") # projet auquel on attribue le budget
        z = MODEL.addVars(n, vtype=GRB.CONTINUOUS, name="z")

        # ajout des contraintes
        MODEL.update()
        MODEL.addConstrs((x[i] <= 1 for i in index_p)) # contrainte x <= 1
        MODEL.addConstr((gp.quicksum(c[i] * x[i] for i in index_p) <= budget)) # contrainte de budget
        MODEL.addConstrs((z[i] == gp.quicksum(z_coefficient[i][j] * x[j] for j in index_p) for i in index_n)) # contrainte sur les utilités

        # ajout de la fonction objectif
        MODEL.setObjective(gp.quicksum(z[i] for i in index_n) / n, GRB.MAXIMIZE)
        MODEL.optimize()

        return MODEL

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


z_coefficient = np.array([[19, 6, 17, 2],
                          [2, 11, 4, 18]])
c = np.array([40, 50, 60, 50])
budget = 100
w1 = [2, 1]
w2 = [10, 1]

selection_1 = selection_multicritere_projet(c, budget, w1, z_coefficient)
selection_2 = selection_multicritere_projet(c, budget, w2, z_coefficient)
seleection_moyenne = selection_multicritere_projet_moyenne(c, budget, z_coefficient)

print("Solution avec w1 =", w1,": ")
print_solution(selection_1)
print("\nSolution avec w2 =", w2,": ")
print_solution(selection_2)
print("\nSolution maximisant la satisfaction moyenne des objectifs : ")
print_solution(seleection_moyenne)