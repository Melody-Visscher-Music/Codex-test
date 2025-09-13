import bpy
from bpy.types import Panel


class BLENDERTOOLS_PT_main(Panel):
    bl_label = "Blender Tools"
    bl_idname = "BLENDERTOOLS_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"

    def draw(self, context):  # pragma: no cover - UI code
        self.layout.label(text="Utilities for Blender")


class _SubPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Tools"
    bl_parent_id = "BLENDERTOOLS_PT_main"


class BLENDERTOOLS_PT_optimize(_SubPanel):
    bl_label = "Optimize"

    def draw(self, context):  # pragma: no cover - UI code
        layout = self.layout
        layout.operator("object.purge_unused_data")


class BLENDERTOOLS_PT_uv(_SubPanel):
    bl_label = "UV"

    def draw(self, context):  # pragma: no cover - UI code
        layout = self.layout
        layout.operator("uv.auto_uv")


class BLENDERTOOLS_PT_materials(_SubPanel):
    bl_label = "Materials"

    def draw(self, context):  # pragma: no cover
        layout = self.layout
        layout.operator("material.create_pbr_template")


class BLENDERTOOLS_PT_baking(_SubPanel):
    bl_label = "Baking"

    def draw(self, context):  # pragma: no cover
        layout = self.layout
        layout.operator("object.bake_preset")


class BLENDERTOOLS_PT_export(_SubPanel):
    bl_label = "Export"

    def draw(self, context):  # pragma: no cover
        layout = self.layout
        layout.operator("export_scene.godot_glb")


class BLENDERTOOLS_PT_animation(_SubPanel):
    bl_label = "Animation"

    def draw(self, context):  # pragma: no cover
        layout = self.layout
        layout.operator("object.push_action_to_nla")


PANELS = [
    BLENDERTOOLS_PT_main,
    BLENDERTOOLS_PT_optimize,
    BLENDERTOOLS_PT_uv,
    BLENDERTOOLS_PT_materials,
    BLENDERTOOLS_PT_baking,
    BLENDERTOOLS_PT_export,
    BLENDERTOOLS_PT_animation,
]


def register():
    for panel in PANELS:
        bpy.utils.register_class(panel)


def unregister():
    for panel in reversed(PANELS):
        bpy.utils.unregister_class(panel)
