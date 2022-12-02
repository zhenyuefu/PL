import gurobipy as gp
from gurobipy import GRB

try:
    MODEL = gp.Model("12")
    z = [4, 7, 1, 3, 9, 2]
    r = MODEL.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
    b = MODEL.addVars(6, vtype=GRB.CONTINUOUS, lb=0, name="b")
    MODEL.update()
    MODEL.addConstrs((r - b[i] <= z[i] for i in range(6)), "z")
    MODEL.setObjective(6*r - gp.quicksum(b), GRB.MAXIMIZE)
    MODEL.optimize()
    print("solution:")
    print("r = ", r.x)
    for i in range(6):
        print("b[", i, "] = ", b[i].x)
    print("objective value = ", MODEL.objVal)


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
