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

def add_quad_diameter(root_node, scale = 0.5, offset = 0.5, path_scale = 1.0):

	# For realistic dendrite thickness special quadratic coefficients are needed
	quad_coefficients = \
	{8:  (0.034881,		-0.6837,	3.6564),
	16:  (0.013947,		-0.51179,	4.9629),
	24:  (0.0064104,	-0.39213,	6.0818),
	32:  (0.0040126,	-0.33498,	7.0306),
	40:  (0.0028541,	-0.2992,	7.8229),
	48:  (0.002163,		-0.27289,	8.5377),
	56:  (0.0017122,	-0.25251,	9.1937),
	64:  (0.0013991,	-0.23611,	9.8033),
	72:  (0.0011712,	-0.22255,	10.375),
	80:  (0.0009992,	-0.21109,	10.915),
	88:  (0.00086562,	-0.20124,	11.428),
	96:  (0.00075942,	-0.19265,	11.917),
	104: (0.00067336,	-0.18507,	12.386),
	112: (0.00060242,	-0.17833,	12.837),
	120: (0.00054315,	-0.17227,	13.271),
	128: (0.00049301,	-0.16678,	13.691),
	136: (0.00045017,	-0.16179,	14.097),
	144: (0.00041319,	-0.15722,	14.49),
	152: (0.00038102,	-0.15301,	14.873),
	160: (0.00035283,	-0.14913,	15.245),
	168: (0.00032796,	-0.14552,	15.608),
	176: (0.00030588,	-0.14216,	15.961),
	184: (0.00028618,	-0.13902,	16.306),
	192: (0.0002685,	-0.13608,	16.644),
	200: (0.00025257,	-0.13332,	16.974),
	208: (0.00023817,	-0.13071,	17.297),
	216: (0.00022508,	-0.12825,	17.613),
	224: (0.00021315,	-0.12593,	17.924),
	232: (0.00020224,	-0.12372,	18.228),
	240: (0.00019222,	-0.12162,	18.527),
	248: (0.00018301,	-0.11963,	18.82),
	256: (0.00017452,	-0.11773,	19.109),
	264: (0.00016666,	-0.11591,	19.392),
	272: (0.00015937,	-0.11418,	19.671),
	280: (0.0001526,	-0.11251,	19.946),
	288: (0.00014629,	-0.11092,	20.216),
	296: (0.00014041,	-0.10939,	20.482),
	304: (0.00013491,	-0.10793,	20.744),
	312: (0.00012976,	-0.10651,	21.002),
	320: (0.00012493,	-0.10515,	21.257),
	360: (0.00010472,	-0.099041,	22.48),
	400: (8.9357e-05,	-0.093832,	23.639),
	440: (7.735e-05,	-0.089314,	24.745),
	480: (6.7797e-05,	-0.085364,	25.793),
	520: (6.0049e-05,	-0.081869,	26.789),
	560: (5.3664e-05,	-0.078748,	27.739),
	600: (4.833e-05,	-0.075937,	28.647),
	640: (4.382e-05,	-0.073387,	29.517),
	680: (3.9968e-05,	-0.071061,	30.351),
	720: (3.6647e-05,	-0.068927,	31.152),
	760: (3.3762e-05,	-0.066959,	31.922),
	800: (3.1236e-05,	-0.065137,	32.664),
	840: (2.9011e-05,	-0.063444,	33.378),
	880: (2.704e-05,	-0.061865,	34.067),
	920: (2.5283e-05,	-0.060388,	34.732),
	960: (2.3712e-05,	-0.059003,	35.373)}

	# Collect all nodes in a list
	nodes = tree_to_list(root_node)
	# Determine terminal nodes
	terminal_nodes = [node for node in nodes if not node.children]
	for terminal_node in terminal_nodes:
		node = terminal_node
		c = quad_coefficients[min(quad_coefficients, key=lambda x:abs(x - terminal_node.path_distance * path_scale))]
		while node is not None:
			x = node.path_distance * path_scale
			if not hasattr(node, 'temp_t'):
				node.temp_t = []
			node.temp_t.append((x**2 * c[0] + x * c[1] + c[2]) * scale)
			node = node.parent

	for node in nodes:
		node.thickness = sum(node.temp_t) / len(node.temp_t)
		del node.temp_t
