import bpy
from bpy.types import Operator


class EXPORT_SCENE_OT_godot_glb(Operator):
    bl_idname = "export_scene.godot_glb"
    bl_label = "Export GLB"
    bl_description = "Export selected objects to GLB for Godot"

    filepath: str = bpy.props.StringProperty(name="File Path", default="//export.glb")
    apply_transforms: bool = bpy.props.BoolProperty(
        name="Apply Transforms", default=True
    )

    def execute(self, context):
        # Real implementation would call bpy.ops.export_scene.gltf
        self.report({"INFO"}, f"Exported to {self.filepath}")
        return {"FINISHED"}


CLASSES = [EXPORT_SCENE_OT_godot_glb]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
