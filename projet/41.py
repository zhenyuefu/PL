# Modeling the shortest path problem

import gurobipy as gp
import networkx as nx
from gurobipy import GRB
from matplotlib import pyplot as plt

# Create an oriented graph
G = nx.DiGraph()

# Add edges
G.add_edge('a', 'b', w=(5, 3))
G.add_edge('a', 'c', w=(10, 4))
G.add_edge('a', 'd', w=(2, 6))
G.add_edge('b', 'c', w=(4, 2))
G.add_edge('b', 'd', w=(1, 3))
G.add_edge('b', 'e', w=(4, 6))
G.add_edge('c', 'e', w=(3, 1))
G.add_edge('c', 'f', w=(1, 2))
G.add_edge('d', 'c', w=(1, 4))
G.add_edge('d', 'f', w=(3, 5))
G.add_edge('e', 'g', w=(1, 1))
G.add_edge('f', 'g', w=(1, 1))

m = gp.Model()
x = gp.tupledict()
s = gp.tupledict()
for i, j in G.edges():
    x[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}')
scenarios = range(2)
for i in scenarios:
    s[i] = m.addVar(vtype=GRB.BINARY, name=f's_{i}')
m.update()

# add constraints
for v in G.nodes():
    if v not in ['a', 'g']:
        m.addConstr(gp.quicksum(x[i, j] for i, j in G.in_edges(v)) == gp.quicksum(x[i, j] for i, j in G.out_edges(v)))

m.addConstr(gp.quicksum(s[i] for i in scenarios) == 1)

m.addConstr(gp.quicksum(x[i, j] for i, j in G.out_edges('a')) == 1)
m.addConstr(gp.quicksum(x[i, j] for i, j in G.in_edges('g')) == 1)

m.setObjective(gp.quicksum(x[i, j] * G[i][j]['w'][k] * s[k] for i, j in G.edges() for k in scenarios),
               GRB.MINIMIZE)
m.update()

m.optimize()

print(f'Optimal value: {m.objVal}')
optimal_scenario = 0
for i in scenarios:
    if s[i].x == 1:
        optimal_scenario = i
        print(f'Optimal scenario: {i + 1}')
        break
for i, j in G.edges():
    if x[i, j].x == 1:
        print(f'Optimal path: {i} -> {j}, cost: {G[i][j]["w"][optimal_scenario]}')

# draw the graph
pos = {'a': (0, 0), 'b': (1, 1), 'c': (2, 0), 'd': (1, -1), 'e': (3, 1), 'f': (3, -1), 'g': (4, 0)}
red_edges = [(i, j) for i, j in G.edges() if x[i, j].x == 1]
edge_colors = ['red' if edge in red_edges else 'black' for edge in G.edges()]
node_colors = ['red' if node == 'a' or node == 'g' else 'white' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)
edge_labels = {(i, j): G[i][j]['w'][optimal_scenario] for i, j in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.6)
plt.axis('off')
plt.savefig('shortest_path_4_1.png')
plt.show()
