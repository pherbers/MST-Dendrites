import mstree
import numpy as np
import cProfile
import csv
import time

f = open('testdata_large.csv', 'r')
reader = csv.reader(f, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
points = np.array([row for row in reader])
v = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
for vv in v:
	points = np.random.rand(vv,2) * 10 - 5
	points[0] = (0,0)
	# cProfile.run('mstree.mstree(points, threshold = 100, balancing_factor = 0.0)')
	t1 = time.time()
	tree = mstree.mstree(points, balancing_factor = 0.0)
	t2 = time.time()
	print(vv, '\t', t2-t1)
# mstree.add_quad_diameter(tree)