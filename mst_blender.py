import mstree
import bpy
import numpy as np
import mathutils
import math
import random

bl_info = {
    "name": "Minumum Spanning Tree",
    "description": "Addon for creating minimum spanning trees",
    "category": "Add Curve",
    "author": "Patrick Herbers"
}

def buildTreeMesh(root_node):

    def buildTreeMeshRecursive(root_node, vertex_index, vertices, edges):
        for child in root_node.children:
            vertices.append(child.pos)
            edges.append([vertex_index, len(vertices) - 1])
            buildTreeMeshRecursive(child, len(vertices) - 1, vertices, edges)

    vertices = [root_node.pos]
    edges = []
    for child in root_node.children:
        vertices.append(child.pos)
        edges.append([0, len(vertices) - 1])
        buildTreeMeshRecursive(child, len(vertices) - 1, vertices, edges)

    mesh = bpy.data.meshes.new("Tree")
    mesh.from_pydata(vertices, edges, [])
    mesh.update()

    obj = bpy.data.objects.new("Tree", mesh)
    bpy.context.scene.objects.link(obj)

def buildTreeCurve(root_node):

    def buildTreeCurveRecursive(root_node, curve, spline):
        spline.bezier_points.add()
        point_index = len(spline.bezier_points) - 1
        point = spline.bezier_points[-1]
        point.co = mathutils.Vector(root_node.pos)
        point.handle_left_type = 'AUTO'
        point.handle_right_type = 'AUTO'

        if len(root_node.children) > 0:
            buildTreeCurveRecursive(root_node.children[0], curve, spline)

        if len(root_node.children) > 1:
            for child in root_node.children[1:]:
                branch = curve.splines.new('BEZIER')
                point_branch = branch.bezier_points[0]
                point_branch.co = mathutils.Vector(root_node.pos)

                buildTreeCurveRecursive(child, curve, branch)
                branch.bezier_points[0].handle_right_type = 'VECTOR'
                branch.bezier_points[0].handle_left_type = 'VECTOR'
            spline.bezier_points[point_index].handle_right_type = 'VECTOR'
            spline.bezier_points[point_index].handle_left_type = 'VECTOR'

    curve = bpy.data.curves.new('Tree', 'CURVE')
    curve.dimensions = '3D'
    
    for child in root_node.children:
        branch = curve.splines.new('BEZIER')
        point = branch.bezier_points[0]
        point.co = mathutils.Vector(root_node.pos)

        buildTreeCurveRecursive(child, curve, branch)
        branch.bezier_points[0].handle_right_type = 'VECTOR'
        branch.bezier_points[0].handle_left_type = 'VECTOR'

    curve_object = bpy.data.objects.new("Tree", curve)
    bpy.context.scene.objects.link(curve_object)

def spinPoints(points, axis, axis_direction, radians = math.pi, seed = None):
    rng = random.Random()
    rng.seed(seed)

    dir_n = axis_direction / np.linalg.norm(axis_direction)
    a = axis[0]; b = axis[1]; c = axis[2]
    u = dir_n[0]; v = dir_n[1]; w = dir_n[2]

    new_points = []

    # Formula: http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/

    for point in points:
        rotation = rng.random() * radians
        x = point[0]; y = point[1]; z = point[2]
        v1 = (a*(v**2 + w**2) - u*(b*v + c*w - u*x - v*y - w*z)) * (1 - np.cos(rotation)) + x*np.cos(rotation) + (-c*v+b*w-w*y+v*z) * np.sin(rotation)
        v2 = (b*(u**2 + w**2) - v*(a*u + c*w - u*x - v*y - w*z)) * (1 - np.cos(rotation)) + y*np.cos(rotation) + (c*u-a*w+w*x+u*z) * np.sin(rotation)
        v3 = (c*(u**2 + v**2) - w*(a*u + b*v - u*x - v*y - w*z)) * (1 - np.cos(rotation)) + z*np.cos(rotation) + (-b*u+a*v-v*x+u*y) * np.sin(rotation)
        new_points.append((v1,v2,v3))

    return np.array(new_points)


class MSTProperties(bpy.types.PropertyGroup):
    balancing_factor = bpy.props.FloatProperty(name = "Balancing factor", default = 0.5, min = 0.0, max = 1.0)

    threshold = bpy.props.FloatProperty(name = "Threshold", default = 50)

    point_data_type = bpy.props.EnumProperty(
        name = "Point data type",
        items = (
            ('PARTICLE', 'Particle system', 'Use the particles of a particle system as points'),
            ('GROUP', 'By layer', 'Use locations of objects in group as points')
        ),
        default = 'PARTICLE'
    )

    source_object = bpy.props.StringProperty(name = "Object")
    source_particle_system = bpy.props.StringProperty(name = "Object")

    root_data_type = bpy.props.EnumProperty(
        name = "Root data type",
        items = (
            ('PARTICLE', 'First Particle', 'Use the first particle in particle system as root point'),
            ('CURSOR', '3D cursor', 'Use 3D cursor location as root point'),
            ('OBJECT', 'Object center', 'Use an object center as root point')
        ),
        default = 'CURSOR'
    )

    root_data_object = bpy.props.StringProperty(name = "Root object")

    build_type = bpy.props.EnumProperty(
        name = "Build type",
        items = (
            ('MESH', 'Mesh', 'Build the tree out of vertices'),
            ('CURVE', 'Curve', 'Build the tree out of curves')
        ),
        default = 'MESH'
    )

    random_spin = bpy.props.BoolProperty(name = "Random spin", default = False)
    spin_object = bpy.props.StringProperty(name = "Axis object")
    spin_degrees = bpy.props.FloatProperty(name = "Spin degrees", subtype = 'ANGLE', min = 0.0, max = 2*math.pi, default = math.pi)
    spin_axis = bpy.props.EnumProperty(name = "Spin axis", items = (('X', 'X', 'Spin along the X-axis of the object'), ('Y', 'Y', 'Spin along the Y-axis of the object'), ('Z', 'Z', 'Spin along the Z-axis of the object')), default = 'Y')

class MSTPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_label = "Minimum Spanning Tree"
    bl_category = "Tools"

    def draw(self, context):
        op = context.scene.mst_options

        layout = self.layout

        row = layout.row()
        row.prop(op, "balancing_factor")
        
        row = layout.row()
        row.prop(op, "point_data_type")
        row = layout.row()
        row.prop_search(op, "source_object", bpy.data, 'objects')
        row = layout.row()
        if op.source_object in bpy.data.objects:
            row.prop_search(op, "source_particle_system", bpy.data.objects[op.source_object], 'particle_systems')

        row = layout.row()
        row.prop(op, "root_data_type")

        if op.root_data_type == 'OBJECT':
            row = layout.row()
            row.prop_search(op, "root_data_object", bpy.data, 'objects')

        row = layout.row()
        row.prop(op, "build_type")

        row = layout.row()
        row.prop(op, "random_spin")

        if op.random_spin:
            row = layout.row()
            row.prop_search(op, "spin_object", bpy.data, 'objects')

            row = layout.row()
            row.prop(op, "spin_degrees")

            row = layout.row()
            row.prop(op, "spin_axis")

        row = layout.row()
        row.operator("object.create_mst")

class CreateMST(bpy.types.Operator):
    bl_idname = "object.create_mst"
    bl_label = "Create MST"

    def execute(self, context):
        print("Creating MST")
        options = context.scene.mst_options

        if options.point_data_type == 'PARTICLE':
            particle_system = bpy.data.objects[options.source_object].particle_systems[0]
            particle_points = [(x.location[0], x.location[1], x.location[2]) for x in particle_system.particles]
            if options.root_data_type == 'OBJECT':
                root_point = bpy.data.objects[options.root_data_object].location
                root_list = [(root_point[0], root_point[1], root_point[2])]
                root_list.extend(particle_points)
                points = np.array(root_list)
            elif options.root_data_type == 'CURSOR':
                root_point = bpy.context.scene.cursor_location
                root_list = [(root_point[0], root_point[1], root_point[2])]
                root_list.extend(particle_points)
                points = np.array(root_list)
            else:
                points = np.array(particle_points)

        if options.random_spin:
            location = bpy.data.objects[options.spin_object].location
            axis = bpy.data.objects[options.spin_object].rotation_quaternion.axis

            if options.spin_axis == 'Y':
                axis.rotate(mathutils.Matrix.Rotation(math.pi / 2, 4, 'Z'))
            elif options.spin_axis == 'Z':
                axis.rotate(mathutils.Matrix.Rotation(math.pi / 2, 4, 'Y'))

            points = spinPoints(points, np.array(location), np.array(axis))

        root_node = mstree.mstree(points, balancing_factor = options.balancing_factor)

        if options.build_type == 'MESH':
            buildTreeMesh(root_node)
        elif options.build_type == 'CURVE':
            buildTreeCurve(root_node)
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MSTProperties)
    bpy.types.Scene.mst_options = bpy.props.PointerProperty(type=MSTProperties)
    bpy.utils.register_class(CreateMST)
    bpy.utils.register_class(MSTPanel)

def unregister():
    bpy.utils.unregister_class(MSTProperties)
    del bpy.types.Scene.mst_options
    bpy.utils.unregister_class(CreateMST)
    bpy.utils.unregister_class(MSTPanel)

if __name__ == '__main__':
    register()