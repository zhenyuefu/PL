import gurobipy as gp
from gurobipy import GRB

MODEL = gp.Model("33")

x = MODEL.addVars(4, 4, vtype=GRB.INTEGER, name="x")

MODEL.addConstrs(
    (
        gp.quicksum(x[i, j + k] for k in range(3)) >= 1
        for i in range(4)
        for j in range(2)
    ),
    "c1",
)
MODEL.addConstrs(
    (
        gp.quicksum(x[i + k, j] for k in range(3)) <= 1
        for i in range(2)
        for j in range(4)
    ),
    "c2",
)

MODEL.setObjective(gp.quicksum(x[i, j] for i in range(4) for j in range(4)))

MODEL.optimize()

print("")
print("Solution optimale:")
for i in range(1, 5):
    print("")
    for j in range(1, 5):
        print(x[i - 1, j - 1].x, end="")
print("")
print("Valeur de la fonction objectif :", MODEL.objVal)
