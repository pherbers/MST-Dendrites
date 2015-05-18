import mstree
import numpy as np
import cProfile
import csv

f = open('testdata_large.csv', 'r')
reader = csv.reader(f, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
points = np.array([row for row in reader])
print(points)
cProfile.run('mstree.mstree(points, threshold = 100, balancing_factor = 0.0)')