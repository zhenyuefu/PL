import numpy as np



u = np.array([[325, 225, 210, 115, 75, 50]])
u = np.repeat(u, 3, axis=0)

x = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0]])
print(u*x)
print((u * x).sum(axis=1))
z = (u * x).sum(axis=1)
r = np.array([0, 0, 300])
b = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
print(r - b)
z = np.reshape(z, (3, 1))
print(z* np.ones((3, 3)))
print((r - b) < z * np.ones((3, 3)))

print(np.arange(4))