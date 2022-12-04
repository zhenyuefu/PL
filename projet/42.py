import gurobipy as gp
import networkx as nx
import numpy as np
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
n = 2
w = [2, 1]
w_prime = [w[i] - w[i + 1] for i in range(n - 1)]
w_prime.append(w[n - 1])
w_prime = np.array(w_prime)
# Create variables
x = gp.tupledict()
for i, j in G.edges():
    x[i, j] = m.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}')
r = m.addMVar(n, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
b = m.addMVar((n, n), vtype=GRB.CONTINUOUS, lb=0, name="b")
k = np.arange(1, n + 1)
m.update()

# add constraints
for v in G.nodes():
    if v not in ['a', 'g']:
        m.addConstr(gp.quicksum(x[i, j] for i, j in G.in_edges(v)) == gp.quicksum(x[i, j] for i, j in G.out_edges(v)))
m.addConstr(gp.quicksum(x[i, j] for i, j in G.out_edges('a')) == 1)
m.addConstr(gp.quicksum(x[i, j] for i, j in G.in_edges('g')) == 1)

# t_i = sum(weight[i,j] * x[i, j] for i, j in G.edges())
t = np.array([gp.quicksum(G.edges[i, j]['w'][k] * x[i, j] for i, j in G.edges()) for k in range(n)])

# r_k - b_i,k + t_i <= 0
for k in range(n):
    for i in range(n):
        m.addConstr(r[k] - b[i, k] + t[i] <= 0)
m.setObjective(sum(w_prime * (r * k - b.sum(axis=0))), GRB.MAXIMIZE)
m.optimize()

print('Obj:', m.objVal)
for i in range(n):
    print(f't_{i + 1} = {t[i].getValue()}')
for i, j in G.edges():
    if x[i, j].x == 1:
        print(f'{i} -> {j} : {x[i, j].x}')

# draw the graph
pos = {'a': (0, 0), 'b': (1, 1), 'c': (2, 0), 'd': (1, -1), 'e': (3, 1), 'f': (3, -1), 'g': (4, 0)}
red_edges = [(i, j) for i, j in G.edges() if x[i, j].x == 1]
edge_colors = ['red' if edge in red_edges else 'black' for edge in G.edges()]
node_colors = ['red' if node == 'a' or node == 'g' else 'white' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)
edge_labels = nx.get_edge_attributes(G, 'w')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.6)
# add the comment
plt.text(0, 1, f'Obj: {m.objVal}', bbox=dict(facecolor='red', alpha=0.5))
for i in range(n):
    plt.text(0, 1-0.12 * (i + 1), f't_{i + 1} = {t[i].getValue()}', bbox=dict(facecolor='red', alpha=0.5))
plt.axis('off')
plt.savefig('path_4_2.png')
plt.show()
