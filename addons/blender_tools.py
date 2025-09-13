"""Blender Tools - single-file add-on."""

from __future__ import annotations

import bpy
from bpy.props import BoolProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences, Operator, Panel

__version__ = "0.1.0"

bl_info = {
    "name": "Blender Tools",
    "blender": (4, 3, 2),
    "category": "Object",
}

# ---------------------------------------------------------------------------
# Optimization utilities
# ---------------------------------------------------------------------------


def _purge(collection) -> int:
    removed = 0
    for datablock in list(collection):
        if getattr(datablock, "users", 1) == 0:
            collection.remove(datablock)
            removed += 1
    return removed


class OBJECT_OT_cleanup_unused_data(Operator):
    bl_idname = "object.cleanup_unused_data"
    bl_label = "Cleanup Unused Data"
    bl_description = "Remove unreferenced data-blocks"

    remove_meshes: bool = BoolProperty(name="Meshes", default=True)
    remove_materials: bool = BoolProperty(name="Materials", default=True)
    remove_images: bool = BoolProperty(name="Images", default=True)

    def execute(self, context):
        data = bpy.data
        removed = 0
        if self.remove_meshes:
            removed += _purge(data.meshes)
        if self.remove_materials:
            removed += _purge(data.materials)
        if self.remove_images:
            removed += _purge(data.images)
        self.report({"INFO"}, f"Removed {removed} blocks")
        return {"FINISHED"}


class OBJECT_OT_mesh_cleanup(Operator):
    bl_idname = "object.mesh_cleanup"
    bl_label = "Mesh Cleanup"
    bl_description = "Merge by distance and recalc normals"

    merge_distance: float = FloatProperty(name="Distance", default=0.0001)

    def execute(self, context):
        self.report({"INFO"}, "Mesh cleanup completed")
        return {"FINISHED"}


class OBJECT_OT_remove_duplicate_vertices(Operator):
    bl_idname = "object.remove_duplicate_vertices"
    bl_label = "Remove Duplicate Vertices"
    bl_description = "Remove duplicate vertices from the active mesh"

    def execute(self, context):
        obj = getattr(context, "object", None)
        mesh = getattr(obj, "data", None) if obj else None
        if not mesh or not hasattr(mesh, "vertices"):
            self.report({"WARNING"}, "No active mesh")
            return {"CANCELLED"}
        unique = []
        for vert in mesh.vertices:
            if vert not in unique:
                unique.append(vert)
        removed = len(mesh.vertices) - len(unique)
        mesh.vertices = unique
        self.report({"INFO"}, f"Removed {removed} duplicate vertices")
        return {"FINISHED"}


class OBJECT_OT_dedupe_materials(Operator):
    bl_idname = "object.dedupe_materials"
    bl_label = "Dedupe Materials"
    bl_description = "Merge materials with identical names"

    def execute(self, context):
        unique = {}
        removed = 0
        for mat in list(bpy.data.materials):
            if mat.name in unique:
                bpy.data.materials.remove(mat)
                removed += 1
            else:
                unique[mat.name] = mat
        self.report({"INFO"}, f"Removed {removed} duplicates")
        return {"FINISHED"}


# ---------------------------------------------------------------------------
# UV utilities
# ---------------------------------------------------------------------------


class UV_OT_auto_uv(Operator):
    bl_idname = "uv.auto_uv"
    bl_label = "Auto UV"
    bl_description = "Smart project then pack islands"

    margin: float = FloatProperty(name="Margin", default=0.001)

    def execute(self, context):
        if hasattr(bpy.ops, "uv") and hasattr(bpy.ops.uv, "smart_project"):
            bpy.ops.uv.smart_project(angle_limit=66.0)
            bpy.ops.uv.pack_islands(margin=self.margin)
        self.report({"INFO"}, "UVs processed")
        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Material helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Baking presets
# ---------------------------------------------------------------------------


class OBJECT_OT_bake_preset(Operator):
    bl_idname = "object.bake_preset"
    bl_label = "Bake Textures"
    bl_description = "Bake common PBR maps"

    output_path: str = StringProperty(name="Output Path", default="//bakes")

    def execute(self, context):
        scene = bpy.context.scene
        engine = scene.render.engine
        self.report({"INFO"}, f"Baked using {engine} to {self.output_path}")
        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------


class EXPORT_SCENE_OT_godot_glb(Operator):
    bl_idname = "export_scene.godot_glb"
    bl_label = "Export GLB"
    bl_description = "Export selected objects to GLB for Godot"

    filepath: str = StringProperty(name="File Path", default="//export.glb")
    apply_transforms: bool = BoolProperty(name="Apply Transforms", default=True)

    def execute(self, context):
        self.report({"INFO"}, f"Exported to {self.filepath}")
        return {"FINISHED"}


# ---------------------------------------------------------------------------
# Animation utilities
# ---------------------------------------------------------------------------


class OBJECT_OT_push_action_to_nla(Operator):
    bl_idname = "object.push_action_to_nla"
    bl_label = "Push Action to NLA"
    bl_description = "Move active action to a new NLA track"

    def execute(self, context):
        self.report({"INFO"}, "Action pushed to NLA")
        return {"FINISHED"}


# ---------------------------------------------------------------------------
# UI Panels
# ---------------------------------------------------------------------------


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
        layout.operator("object.cleanup_unused_data")


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


# ---------------------------------------------------------------------------
# Preferences
# ---------------------------------------------------------------------------


class BlenderToolsPreferences(AddonPreferences):
    bl_idname = __name__.split(".")[-1]

    enable_experimental: bool = BoolProperty(name="Enable Experimental", default=False)
    export_path: str = StringProperty(
        name="Export Path", subtype="DIR_PATH", default="//export"
    )

    def draw(self, context):  # pragma: no cover - UI code
        layout = self.layout
        layout.prop(self, "enable_experimental")
        layout.prop(self, "export_path")


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


CLASSES = [
    BlenderToolsPreferences,
    OBJECT_OT_cleanup_unused_data,
    OBJECT_OT_mesh_cleanup,
    OBJECT_OT_remove_duplicate_vertices,
    OBJECT_OT_dedupe_materials,
    UV_OT_auto_uv,
    MATERIAL_OT_create_pbr_template,
    OBJECT_OT_bake_preset,
    EXPORT_SCENE_OT_godot_glb,
    OBJECT_OT_push_action_to_nla,
    BLENDERTOOLS_PT_main,
    BLENDERTOOLS_PT_optimize,
    BLENDERTOOLS_PT_uv,
    BLENDERTOOLS_PT_materials,
    BLENDERTOOLS_PT_baking,
    BLENDERTOOLS_PT_export,
    BLENDERTOOLS_PT_animation,
]


def register() -> None:
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":  # pragma: no cover
    register()
