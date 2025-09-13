import bpy
from bpy.types import Operator


class MATERIAL_OT_create_pbr_template(Operator):
    bl_idname = "material.create_pbr_template"
    bl_label = "Create PBR Template"
    bl_description = "Create a material with PBR channels"

    def execute(self, context):
        mat = bpy.data.materials.new(name="PBR Material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        output = nodes.new("ShaderNodeOutputMaterial")
        principled = nodes.new("ShaderNodeBsdfPrincipled")
        nodes.new("ShaderNodeTexImage").name = "Base Color"
        nodes.new("ShaderNodeTexImage").name = "ORM"
        nodes.new("ShaderNodeTexImage").name = "Normal"
        nodes.new("ShaderNodeTexImage").name = "Emission"
        if getattr(principled, "outputs", None) and getattr(output, "inputs", None):
            mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
        self.report({"INFO"}, f"Material '{mat.name}' created")
        return {"FINISHED"}


CLASSES = [MATERIAL_OT_create_pbr_template]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
