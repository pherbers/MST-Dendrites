import math
import random
import numpy as np
import matplotlib.pyplot as plt

def mstree(points, balancing_factor = 0.5, threshold = 50):
	length = len(points)
	dimensions = len(points[0])

	root = points[0]

	# Init distance to root
	
	distances_squared = np.sum(np.square(points - root), axis = 1)
	distances = np.sqrt(distances_squared)

	print(distances)


def euclidean_distance(point_a, point_b):
	dist = 0
	for i in range(len(point_a)):
		dist += (point_a[i] - point_b[i]) ** 2
	return sqrt(dist)

if __name__ == '__main__':
	np.fromfunction(lambda i, j: i == j, (3, 3), dtype=int)
	points = np.random.rand(100,3) * 100
	print(points)
	# plt.scatter(points[:,0], points[:,1])
	# plt.show()
	mstree(points)