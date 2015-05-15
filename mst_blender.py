import mstree
import bpy
import numpy as np

bl_info = {
    "name": "Minumum Spanning Tree",
    "description": "Addon for creating minimum spanning trees",
    "category": "Add Curve",
    "author": "Patrick Herbers"
}

def buildTreeRecursive(root_node, vertex_index, vertices, edges):
    for child in root_node.children:
        vertices.append(child.pos)
        edges.append([vertex_index, len(vertices) - 1])
        buildTreeRecursive(child, len(vertices) - 1, vertices, edges)

def buildTree(root_node):
    vertices = [root_node.pos]
    edges = []
    for child in root_node.children:
        vertices.append(child.pos)
        edges.append([0, len(vertices) - 1])
        buildTreeRecursive(child, len(vertices) - 1, vertices, edges)

    mesh = bpy.data.meshes.new("Tree")
    mesh.from_pydata(vertices, edges, [])
    mesh.update()

    obj = bpy.data.objects.new("Tree", mesh)
    bpy.context.scene.objects.link(obj)


class CreateMST(bpy.types.Operator):
    bl_idname = "object.create_mst"
    bl_label = "Create MST"

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

    def execute(self, context):
        print("Creating MST")
        if self.point_data_type == 'PARTICLE':
            particle_system = bpy.data.objects[self.source_object].particle_systems[0]
            particle_points = [(x.location[0], x.location[1], x.location[2]) for x in particle_system.particles]
            if self.root_data_type == 'OBJECT':
                root_point = bpy.data.objects[self.root_data_object].location
                root_list = [(root_point[0], root_point[1], root_point[2])]
                root_list.extend(particle_points)
                points = np.array(root_list)
            elif self.root_data_type == 'CURSOR':
                root_point = bpy.context.scene.cursor_location
                root_list = [(root_point[0], root_point[1], root_point[2])]
                root_list.extend(particle_points)
                points = np.array(root_list)
            else:
                points = np.array(particle_points)

            root_node = mstree.mstree(points, balancing_factor = self.balancing_factor)
            
            buildTree(root_node)

        return {'FINISHED'}

    def invoke(self, context, event):
        active_object = bpy.context.scene.objects.active
        if active_object:
            self.source_object = active_object.name
            self.root_data_object = active_object.name
            if len(active_object.particle_systems) > 0:
                self.source_particle_system = active_object.particle_systems[0].name
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "balancing_factor")
        
        row = layout.row()
        row.prop(self, "point_data_type")
        row = layout.row()
        row.prop_search(self, "source_object", bpy.data, 'objects')
        row = layout.row()
        if self.source_object in bpy.data.objects:
            row.prop_search(self, "source_particle_system", bpy.data.objects[self.source_object], 'particle_systems')

        row = layout.row()
        row.prop(self, "root_data_type")

        if self.root_data_type == 'OBJECT':
            row = layout.row()
            row.prop(self, "root_data_object")

def register():
    bpy.utils.register_class(CreateMST)

def unregister():
    bpy.utils.unregister_class(CreateMST)

if __name__ == '__main__':
    register()