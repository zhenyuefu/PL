import gurobipy as gp
from gurobipy import GRB

try:
    # definition du modele
    # probleme max-X Sudoku
    # trouver une solution du Sudoku 4*4 qui maximise la somme des termes contenus dans deux diagonales
    MODEL = gp.Model("Sudoku")

    # do a systematic search for the k- best solutions
    MODEL.setParam(GRB.Param.PoolSearchMode, 2)

    # sudoku 4*4
    # * 2 * 4
    # 3 * * *
    # * * 4 *
    # * * * *

    n_rows = 4
    n_cols = n_rows
    width_block = 2

    rows = range(n_rows)
    cols = range(n_cols)
    numbers = range(1, n_rows + 1)

    # definition des variables
    # x[i,j,k] = 1 si la case (i,j) contient le nombre k
    x = MODEL.addVars(rows, cols, numbers, vtype=GRB.BINARY, name="x")

    MODEL.update()

    # definition des contraintes
    # 已经有的数字
    MODEL.addConstr(x[0, 1, 2] == 1, "c1")
    MODEL.addConstr(x[0, 3, 4] == 1, "c2")
    MODEL.addConstr(x[1, 0, 3] == 1, "c3")
    MODEL.addConstr(x[2, 2, 4] == 1, "c4")
    # 每一个格子只能填一个数字
    MODEL.addConstrs((x.sum(i, j, "*") == 1 for i in rows for j in cols), "value")
    # 每一个数字在一行中出现一次
    MODEL.addConstrs((x.sum(i, "*", k) == 1 for i in rows for k in numbers), "row")
    # 每个数字在一列中出现一次
    MODEL.addConstrs((x.sum("*", j, k) == 1 for j in cols for k in numbers), "col")
    # 每个数字在一个宫格中出现一次
    MODEL.addConstrs(
        (gp.quicksum(x[i, j, k] for i in range(i0 * width_block, (i0 + 1) * width_block) for j in
                     range(j0 * width_block, (j0 + 1) * width_block)) == 1
         for k in numbers for i0 in range(n_rows // width_block) for j0 in range(n_cols // width_block))
        , "block")

    # definition de la fonction objective
    # 对角线上的数字之和最大
    MODEL.setObjective(gp.quicksum(k * x[i, i, k] + k * x[n_cols - 1 - i, i, k] for i in rows for k in numbers),
                       GRB.MINIMIZE)

    # resolution
    MODEL.optimize()

    # print all solutions
    print("All solutions:")
    for sol in range(MODEL.SolCount):
        MODEL.setParam(GRB.Param.SolutionNumber, sol)
        print('Obj: %g' % MODEL.PoolObjVal)
        for i in rows:
            for j in cols:
                for k in numbers:
                    if x[i, j, k].Xn > 0.5:
                        print(k, end=" ")
            print()


except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
