import gurobipy as gp
from gurobipy import GRB
from numpy import array
from pylab import plot, show

MODEL = gp.Model("34")

x = array([4, 17, 37, 55, 88, 14])
y = [11, 25, 46, 48, 65, 97]

w0 = MODEL.addVar(vtype=GRB.CONTINUOUS, lb=0, name="w0")
w1 = MODEL.addVar(vtype=GRB.CONTINUOUS, lb=0, name="w1")
z = MODEL.addVars(7, vtype=GRB.CONTINUOUS, lb=0, name="z")

MODEL.addConstrs((z[i] >= y[i] - (w1 + w0 * x[i]) for i in range(6)), "c1")
MODEL.addConstrs((z[i] >= (w1 + w0 * x[i]) - y[i] for i in range(6)), "c2")

MODEL.setObjective(gp.quicksum(z[i] for i in range(6)), GRB.MINIMIZE)

MODEL.optimize()

print("")
print("Solution optimale:")
print("w0", "=", w0.x)
print("w1", "=", w1.x)
print("")
print("Valeur de la fonction objectif :", MODEL.objVal)

yhat = w0.x * x + w1.x
line = plot(x, yhat, "r-", x, y, "o")
show()
