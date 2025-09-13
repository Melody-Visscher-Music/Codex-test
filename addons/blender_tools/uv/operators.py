import bpy
from bpy.types import Operator


class UV_OT_auto_uv(Operator):
    bl_idname = "uv.auto_uv"
    bl_label = "Auto UV"
    bl_description = "Smart project then pack islands"

    margin: float = bpy.props.FloatProperty(name="Margin", default=0.001)

    def execute(self, context):
        if hasattr(bpy.ops, "uv") and hasattr(bpy.ops.uv, "smart_project"):
            bpy.ops.uv.smart_project(angle_limit=66.0)
            bpy.ops.uv.pack_islands(margin=self.margin)
        self.report({"INFO"}, "UVs processed")
        return {"FINISHED"}


CLASSES = [UV_OT_auto_uv]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
