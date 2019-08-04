from . import mst_blender
import bpy

bl_info = {
    "name": "Minimum Spanning Tree (MST)",
    "description": "Addon for creating minimum spanning trees",
    "category": "Add Curve",
    "author": "Patrick Herbers",
    "blender": (2, 80, 0),
}

classes = (
	mst_blender.OBJECT_OT_mstadd,
)

register, unregister = bpy.utils.register_classes_factory(classes)
