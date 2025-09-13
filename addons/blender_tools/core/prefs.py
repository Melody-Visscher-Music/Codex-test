import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import AddonPreferences


class BlenderToolsPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]

    enable_experimental: BoolProperty(
        name="Enable Experimental",
        default=False,
    )
    export_path: StringProperty(
        name="Export Path",
        subtype="DIR_PATH",
        default="//export",
    )

    def draw(self, context):  # pragma: no cover - UI code
        layout = self.layout
        layout.prop(self, "enable_experimental")
        layout.prop(self, "export_path")


def register():
    bpy.utils.register_class(BlenderToolsPreferences)


def unregister():
    bpy.utils.unregister_class(BlenderToolsPreferences)
