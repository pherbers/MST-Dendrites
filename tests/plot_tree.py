import matplotlib.pyplot as plt
import mstree
import numpy as np

def drawTree(root_node):
	plt.figure()
	plt.scatter(points[:,0], points[:,1])
	drawTreeRecursive(root_node)
	plt.show()

def drawTreeRecursive(root_node):
	for child in root_node.children:
		print('Plotting from point ' + str(root_node.index) + ' to ' + str(child.index))
		plt.plot((root_node.pos[0], child.pos[0]), (root_node.pos[1], child.pos[1]),'-')
		drawTreeRecursive(child)

if __name__ == '__main__':
	points = np.random.rand(100,2) * 10 - 5
	points[0] = (0,0)
	# plt.scatter(points[:,0], points[:,1])
	# plt.show()
	# f = open('testdata.csv', 'r')
	# reader = csv.reader(f, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	# points = np.array([row for row in reader])
	# print(points)
	root = mstree.mstree(points, threshold = 50, balancing_factor = 0)
	drawTree(root)