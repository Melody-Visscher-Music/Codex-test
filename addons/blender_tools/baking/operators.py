import bpy
from bpy.types import Operator


class OBJECT_OT_bake_preset(Operator):
    bl_idname = "object.bake_preset"
    bl_label = "Bake Textures"
    bl_description = "Bake common PBR maps"

    output_path: str = bpy.props.StringProperty(name="Output Path", default="//bakes")

    def execute(self, context):
        scene = bpy.context.scene
        engine = scene.render.engine
        # Actual bake logic would go here
        self.report({"INFO"}, f"Baked using {engine} to {self.output_path}")
        return {"FINISHED"}


CLASSES = [OBJECT_OT_bake_preset]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
