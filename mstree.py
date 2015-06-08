import numpy as np

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

		open_points = points[open_list]
		weighted_distance = np.sqrt(np.sum(np.square(np.subtract(open_points, location)), axis = 1)) + balancing_factor * path_distance
		open_distance_list_indeces = np.argmin(np.column_stack((open_distance_list, weighted_distance)), axis = 1)
		open_distance_list = np.minimum(open_distance_list, weighted_distance)
		changed_values = np.zeros(len(closest_point_in_tree), dtype = np.bool)
		changed_values.put(open_list, open_distance_list_indeces)
		closest_point_in_tree = np.where(changed_values == 1, point_index, closest_point_in_tree)

	return root_node

def tree_to_list(root_node):
	"""Orders the nodes into a list recursivly using depth-first-search"""
	ls = [root_node]
	for child in root_node.children:
		ls.extend(tree_to_list(child))
	return ls

def add_quad_diameter(root_node, scale = 0.5, offset = 0.5):

	# For realistic dendrite thickness special quadratic coefficients are needed
	quad_coefficients = \
	{8:  (0.0349, -0.6837,  3.6564),
	16:  (0.0139, -0.5118,  4.9629),
	24:  (0.0064, -0.3921,  6.0818),
	32:  (0.0040, -0.3350,  7.0306),
	40:  (0.0029, -0.2992,  7.8229),
	48:  (0.0022, -0.2729,  8.5377),
	56:  (0.0017, -0.2525,  9.1937),
	64:  (0.0014, -0.2361,  9.8033),
	72:  (0.0012, -0.2226, 10.3750),
	80:  (0.0010, -0.2111, 10.9151),
	88:  (0.0009, -0.2012, 11.4279),
	96:  (0.0008, -0.1926, 11.9174),
	104: (0.0007, -0.1851, 12.3862),
	112: (0.0006, -0.1783, 12.8368),
	120: (0.0005, -0.1723, 13.2711),
	128: (0.0005, -0.1668, 13.6905),
	136: (0.0005, -0.1618, 14.0966),
	144: (0.0004, -0.1572, 14.4904),
	152: (0.0004, -0.1530, 14.8730),
	160: (0.0004, -0.1491, 15.2451),
	168: (0.0003, -0.1455, 15.6077),
	176: (0.0003, -0.1422, 15.9612),
	184: (0.0003, -0.1390, 16.3065),
	192: (0.0003, -0.1361, 16.6438),
	200: (0.0003, -0.1333, 16.9738),
	208: (0.0002, -0.1307, 17.2968),
	216: (0.0002, -0.1283, 17.6134),
	224: (0.0002, -0.1259, 17.9236),
	232: (0.0002, -0.1237, 18.2280),
	240: (0.0002, -0.1216, 18.5268),
	248: (0.0002, -0.1196, 18.8203),
	256: (0.0002, -0.1177, 19.1087),
	264: (0.0002, -0.1159, 19.3922),
	272: (0.0002, -0.1142, 19.6711),
	280: (0.0002, -0.1125, 19.9456),
	288: (0.0001, -0.1109, 20.2158),
	296: (0.0001, -0.1094, 20.4818),
	304: (0.0001, -0.1079, 20.7440),
	312: (0.0001, -0.1065, 21.0023),
	320: (0.0001, -0.1052, 21.2570),
	360: (0.0001, -0.0990, 22.4797),
	400: (0.0001, -0.0938, 23.6390),
	440: (0.0001, -0.0893, 24.7449),
	480: (0.0001, -0.0854, 25.7929),
	520: (0.0001, -0.0819, 26.7893),
	560: (0.0001, -0.0787, 27.7393),
	600: (0.0000, -0.0759, 28.6473),
	640: (0.0000, -0.0734, 29.5167),
	680: (0.0000, -0.0711, 30.3507),
	720: (0.0000, -0.0689, 31.1517),
	760: (0.0000, -0.0670, 31.9220),
	800: (0.0000, -0.0651, 32.6636),
	840: (0.0000, -0.0634, 33.3782),
	880: (0.0000, -0.0619, 34.0671),
	920: (0.0000, -0.0604, 34.7317),
	960: (0.0000, -0.0590, 35.3733)}

	# Collect all nodes in a list
	nodes = tree_to_list(root_node)
	# Determine terminal nodes
	terminal_nodes = [node for node in nodes if not node.children]
	for terminal_node in terminal_nodes:
		node = terminal_node
		c = quad_coefficients[min(quad_coefficients, key=lambda x:abs(x - terminal_node.path_distance))]
		while node is not None:
			x = node.path_distance
			if not hasattr(node, 'temp_t'):
				node.temp_t = []
			node.temp_t.append((x**2 * c[0] + x * c[1] + c[2]) * scale)
			node = node.parent

	for node in nodes:
		node.thickness = sum(node.temp_t) / len(node.temp_t)
		del node.temp_t

	import pdb
	pdb.set_trace()
