import mstree
import bpy
import numpy as np
import mathutils

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
            buildTreeRecursive(child, len(vertices) - 1, vertices, edges)

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

        root_node = mstree.mstree(points, balancing_factor = options.balancing_factor)

        if options.build_type == 'MESH':
            buildTreeMesh(root_node)
        elif options.build_type == 'CURVE':
            buildTreeCurve(root_node)
        
        return {'FINISHED'}

    # def invoke(self, context, event):
    #     active_object = bpy.context.scene.objects.active
    #     if active_object:
    #         self.source_object = active_object.name
    #         self.root_data_object = active_object.name
    #         if len(active_object.particle_systems) > 0:
    #             self.source_particle_system = active_object.particle_systems[0].name
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)


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