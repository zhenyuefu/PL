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

        # ajout des variables
        x = MODEL.addVars(p, vtype=GRB.BINARY, name="x") # projet auquel on attribue le budget
        r = MODEL.addVars(n, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
        b = MODEL.addVars(n, n, vtype=GRB.CONTINUOUS, lb=0, name="b")
        z = [sum(u[i][j] * x[j] for j in range(p)) for i in range(n)]

        # ajout des contraintes
        MODEL.update()
        MODEL.addConstrs((x[i] <= 1 for i in range(p))) # contrainte x <= 1
        MODEL.addConstr((gp.quicksum(c[i] * x[i] for i in range(p)) <= budget)) # contrainte de budget
        MODEL.addConstrs((r[k] - b[i, k] <= z[i] for i in range(n) for k in range(n)))

        # ajout de la fonction objectif
        MODEL.setObjective(gp.quicksum(w_prime[k] * ((k+1) * r[k] - gp.quicksum(b[i, k] for i in range(n))) for k in range(n)),
                        GRB.MAXIMIZE)
        MODEL.optimize()
        
        return MODEL, x, z

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')


def selection_multicritere_projet_moyenne(c, budget, u):
    """
    :param c: liste des coûts des projets
    :param budget: budget à ne pas dépasser
    :param u: matrice des utilités de chaque projet pour chaque objectif
    """
    try:
        MODEL = gp.Model("31")
        n = len(u) # nombre d'objectif
        p = len(c) # nombre de projet

        # ajout des variables
        x = MODEL.addVars(p, vtype=GRB.BINARY, name="x") # projet auquel on attribue le budget
        z = [sum(u[i][j] * x[j] for j in range(p)) for i in range(n)]

        # ajout des contraintes
        MODEL.update()
        MODEL.addConstrs((x[i] <= 1 for i in range(p))) # contrainte x <= 1
        MODEL.addConstr((gp.quicksum(c[i] * x[i] for i in range(p)) <= budget)) # contrainte de budget

        # ajout de la fonction objectif
        MODEL.setObjective(gp.quicksum(z[i] for i in range(n)) / n, GRB.MAXIMIZE)
        MODEL.optimize()

        return MODEL, x, z

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

def print_solution(MODEL, x, z):
    if MODEL.status == GRB.OPTIMAL:
            print("solution:")
            for i in range(len(z)):
                print(f"z[{i+1}] = {z[i].getValue()}")
            print()
            for i in range(len(x)):
                print(f"x[{i+1}] = {x[i].x}", end=" ")
                print()
            print("objective value = ", MODEL.objVal)
    else:
        print("No solution")
    # print solution time
    print("solution time = ", MODEL.Runtime, "s")

u = np.array([[19, 6, 17, 2],
              [2, 11, 4, 18]])
c = np.array([40, 50, 60, 50])
budget = 100
w1 = [2, 1]
w2 = [10, 1]

selection_1,z1,x1 = selection_multicritere_projet(c, budget, w1, u)
selection_2,z2,x2 = selection_multicritere_projet(c, budget, w2, u)
selection_moyenne,z3,x3 = selection_multicritere_projet_moyenne(c, budget, u)

print("w =", w1)
print("Solution avec w1:")
print_solution(selection_1, z1, x1)

print("\nw =", w2)
print("Solution avec w2 =:")
print_solution(selection_2, z2, x2)

print("\nSolution maximisant la satisfaction moyenne des objectifs:")
print_solution(selection_moyenne, z3, x3)
