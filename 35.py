import gurobipy as gp
from gurobipy import GRB

MODEL = gp.Model("35")
x = MODEL.addVars(3, vtype=GRB.CONTINUOUS, name="x")
MODEL.addConstr(x[0] + 2 * x[1] + 3 * x[2] >= 8, "c1")
MODEL.addConstr(3 * x[0] + x[1] + x[2] >= 5, "c2")

MODEL.setObjective(7 * x[0] + 3 * x[1] + 4 * x[2], GRB.MINIMIZE)

MODEL.optimize()

print("")
print("Solution optimale:")
print("x1", "=", x[0].x)
print("x2", "=", x[1].x)
print("x3", "=", x[2].x)
print("")
print("Valeur de la fonction objectif :", MODEL.objVal)

P1 = gp.Model("P1")
x1 = P1.addVars(2, vtype=GRB.CONTINUOUS, name="x1")
P1.addConstr(x1[0] + 6 + 3 * x1[1] >= 8, "c1")
P1.addConstr(3 * x1[0] + 3 + x1[1] >= 5, "c2")

P1.setObjective(7 * x1[0] + 9 + 4 * x1[1], GRB.MINIMIZE)

P1.optimize()

print("")
print("Solution optimale:")
print("x1", "=", x1[0].x)
print("x3", "=", x1[1].x)
print("")
print("Valeur de la fonction objectif :", P1.objVal)

P2 = gp.Model("P2")
x2 = P2.addVars(2, vtype=GRB.CONTINUOUS, name="x2")
P2.addConstr(x2[0] + 8 + 3 * x2[1] >= 8, "c1")
P2.addConstr(3 * x2[0] + 4 + x2[1] >= 5, "c2")

P2.setObjective(7 * x2[0] + 12 + 4 * x2[1], GRB.MINIMIZE)

P2.optimize()

print("")
print("Solution optimale:")
print("x1", "=", x2[0].x)
print("x3", "=", x2[1].x)
print("")
print("Valeur de la fonction objectif :", P2.objVal)

P3 = gp.Model("P1")
x3 = P3.addVars(2, vtype=GRB.CONTINUOUS, name="x3")
P3.addConstr(2 * x3[0] + 3 * x3[1] >= 8, "c1")
P3.addConstr(x3[0] + x3[1] >= 5, "c2")

P3.setObjective(3 * x3[0] + 4 * x3[1], GRB.MINIMIZE)

P3.optimize()

print("")
print("Solution optimale:")
print("x2", "=", x3[0].x)
print("x3", "=", x3[1].x)
print("")
print("Valeur de la fonction objectif :", P3.objVal)

S = gp.Model("S")
xs = S.addVars(3, vtype=GRB.INTEGER, name="xs")
S.addConstr(xs[0] + 2 * xs[1] + 3 * xs[2] >= 8, "c1")
S.addConstr(3 * xs[0] + xs[1] + xs[2] >= 5, "c2")

S.setObjective(7 * xs[0] + 3 * xs[1] + 4 * xs[2], GRB.MINIMIZE)

S.optimize()

print("")
print("Solution optimale:")
print("x1", "=", xs[0].x)
print("x2", "=", xs[1].x)
print("x3", "=", xs[2].x)
print("")
print("Valeur de la fonction objectif :", S.objVal)

D = gp.Model("Dual")
y = D.addVars(2, vtype=GRB.CONTINUOUS, name="y")
D.addConstr(y[0] + 3 * y[1] <= 7, "c1")
D.addConstr(2 * y[0] + y[1] <= 3, "c2")
D.addConstr(3 * y[0] + y[1] <= 4, "c3")

D.setObjective(8 * y[0] + 5 * y[1], GRB.MAXIMIZE)

D.optimize()

print("")
print("Solution optimale:")
print("y1", "=", y[0].x)
print("y2", "=", y[1].x)
print("")
print("Valeur de la fonction objectif :", D.objVal)
