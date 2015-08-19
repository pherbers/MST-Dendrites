# MST-Dendrites
Realistic artificial dendrites using minimum spanning trees and Blender 3D. A short tutorial on how to use it can be found [here](https://youtu.be/yTYr22yE2OQ).

## mstree.py
mstree.py gives access to functions for creating minimum spanning trees with balancing factor. The work is based on [a paper for synthetic neuronal structures](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000877) by Hermann Cuntz.
Given a set of points, the algorithm calculates a minimum spanning tree on them.

## Blender Addon
mst_blender is an addon for [Blender 3D](blender.org) to create minimum spanning trees directly in Blender.
To install, copy the mst_blender folder into your Blender script directory (minimum Blender version 2.70). 
Two new GUI-Panels will show up in your Tools panel, where you can adjust settings for your MST.

This addon was mainly developed to create Dendritic structures in Blender as a bachelor thesis, but it can be used to just create minimum spanning trees when using a balancing factor of 0.
