import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

matplotlib.use('tkagg')
original_stdout = sys.stdout

ey = np.linspace(0, 1, 8)

lle = []
all_inner_neighbours = []
all_neighbours = []

lengths = [0, 0, 0]

for i in ey:
    for u in ey:
        for t in ey:
            lle.append([i, u, t])

lle = np.array(lle)
lle = np.unique(lle, axis=0)

corner = np.array([1, 1, 1])
origo = np.array([0, 0, 0])
mid = np.array([0.5, 0.5, 0.5])


def calc_dist(p1, p2):
    return np.linalg.norm(p1 - p2)


delete_list = []

for i, point in enumerate(lle):
    if calc_dist(point, corner) < 0.5:
        delete_list.append(i)

for i, point in enumerate(lle):
    if calc_dist(point, corner) > 1.2:
        delete_list.append(i)

for i, point in enumerate(lle):
    if calc_dist(point, origo) < 1:
        delete_list.append(i)

for i, point in enumerate(lle):
    if calc_dist(point, mid) > 0.7:
        delete_list.append(i)

for i, point in enumerate(lle):
    if calc_dist(point, mid) < 0.3:
        delete_list.append(i)

lle = np.delete(lle, delete_list, axis=0)
lle = np.round(lle, 3)


for i, point1 in enumerate(lle):
    inner_neighbours = []
    neighbours = []
    for u, point2 in enumerate(lle):
        if i != u:
            dist = calc_dist(point1, point2)
            if dist < 0.16:
                inner_neighbours.append(u)
            elif dist < 0.2:
                neighbours.append(u)
    lengths[1] += len(inner_neighbours)
    lengths[2] += len(neighbours)
    all_inner_neighbours.append(inner_neighbours)
    all_neighbours.append(neighbours)

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(lle[:, 0], lle[:, 1], lle[:, 2], c=lle, depthshade=True)
plt.show()

lle = lle.tolist()
lengths[0] = len(lle)
print(lengths)
print(lle)
print(all_inner_neighbours)
print(all_neighbours)

with open('Colors.swift', 'w') as f:
    sys.stdout = f

    print("import Foundation")
    print("import SpriteKit")
    print()
    print("struct Colors{")
    print("   let pool: [[CGFloat]] =", end=" ")
    print(lle)
    print("   let inner_neighbours: [[Int]] =", end=" ")
    print(all_inner_neighbours)
    print("   let neighbours: [[Int]] =", end=" ")
    print(all_neighbours)
    print("}")
    # f.write('readme')
    f.close()
