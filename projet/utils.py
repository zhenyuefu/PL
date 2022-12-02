from gurobipy import GRB


def print_solution(model):
    if model.status == GRB.OPTIMAL:
        print("solution:")
        for v in model.getVars():
            print(v.varName, "=", v.x)
        print("objective value = ", model.objVal)
    else:
        print("No solution")
    # print solution time
    print("solution time = ", model.Runtime, "s")
