import math
import random
import numpy as np
import csv

class Node:
	def __init__(self, parent, pos, index, path_distance = 0.0):
		self.parent = parent
		self.pos = pos
		self.index = index
		self.children = []
		self.path_distance = path_distance

		if parent is not None:
			parent.children.append(self)

def mstree(points, balancing_factor = 0.5, threshold = 50):
	length = len(points)
	dimensions = len(points[0])

	closed_list = {}

	root_point = points[0]

	root_node = Node(None, root_point, 0)
	closed_list[0] = root_node

	# Init open points list
	open_list = [x for x in range(1,length)]

	# Init distance to root_point
	threshold_squared = threshold ** 2
	distances_squared = np.sum(np.square(points - root_point), axis = 1)
	distances = np.empty(length)
	for i in range(length - 1):
		if distances_squared[i] <= threshold_squared:
			distances[i] = np.sqrt(distances_squared[i])
		else:
			distances[i] = np.nan

	closest_point_in_tree = np.zeros(length, dtype = np.int)
	
	distances = np.sqrt(distances_squared)

	open_distance_list = distances.copy()[1:]
	
	tthreshold = threshold

	while len(open_distance_list) > 0:
		minimum_index = np.argmin(open_distance_list)
		minimum = open_distance_list[minimum_index]
		point_index = open_list.pop(minimum_index)

		# Get closest point and append new node to it
		closest_point_index = closest_point_in_tree[point_index]

		location = points[point_index]

		parent_node = closed_list[closest_point_index]
		actual_distance = np.sqrt(np.sum(np.square(location - parent_node.pos)))
		path_distance = actual_distance + parent_node.path_distance
		node = Node(parent_node, location, point_index, path_distance)
		
		# Add to closed list
		closed_list[point_index] = node
		# Remove from open list
		open_distance_list = np.delete(open_distance_list, minimum_index)

		tthreshold = max(tthreshold, threshold + distances[point_index])

		for open_index_index, open_index in enumerate(open_list):
			dis = open_distance_list[open_index_index]
			weighted_distance = np.sqrt(np.sum(np.square(points[open_index] - location))) + balancing_factor * path_distance
			if dis > weighted_distance:
				open_distance_list[open_index_index] = weighted_distance
				closest_point_in_tree[open_index] = point_index

	return root_node


