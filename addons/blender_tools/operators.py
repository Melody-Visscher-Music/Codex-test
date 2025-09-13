"""Example operators for the Blender Tools add-on."""

import logging

import bpy

from . import optimization

logger = logging.getLogger(__name__)


class OBJECT_OT_hello(bpy.types.Operator):
    """Say hello in the info log."""

    bl_idname = "object.hello"
    bl_label = "Say Hello"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):  # type: ignore[override]
        logger.info("Executing hello operator")
        self.report({"INFO"}, "Hello World")
        return {"FINISHED"}


class OBJECT_OT_cleanup_unused_data(bpy.types.Operator):
    """Remove unused meshes, materials and images."""

    bl_idname = "object.cleanup_unused_data"
    bl_label = "Cleanup Unused Data"

    remove_meshes: bpy.props.BoolProperty = bpy.props.BoolProperty(
        name="Meshes", default=True
    )
    remove_materials: bpy.props.BoolProperty = bpy.props.BoolProperty(
        name="Materials", default=True
    )
    remove_images: bpy.props.BoolProperty = bpy.props.BoolProperty(
        name="Images", default=True
    )

    def execute(self, context):  # type: ignore[override]
        types = []
        if self.remove_meshes:
            types.append("meshes")
        if self.remove_materials:
            types.append("materials")
        if self.remove_images:
            types.append("images")
        removed = optimization.cleanup_unused_data(types)
        self.report({"INFO"}, f"Removed {removed} unused data-blocks")
        return {"FINISHED"}


class OBJECT_OT_remove_duplicate_vertices(bpy.types.Operator):
    """Remove duplicate vertices from all meshes."""

    bl_idname = "object.remove_duplicate_vertices"
    bl_label = "Remove Duplicate Vertices"

    def execute(self, context):  # type: ignore[override]
        removed = optimization.remove_duplicate_vertices_from_meshes()
        self.report({"INFO"}, f"Removed {removed} duplicate vertices")
        return {"FINISHED"}


def register() -> None:
    for cls in (
        OBJECT_OT_hello,
        OBJECT_OT_cleanup_unused_data,
        OBJECT_OT_remove_duplicate_vertices,
    ):
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in (
        OBJECT_OT_remove_duplicate_vertices,
        OBJECT_OT_cleanup_unused_data,
        OBJECT_OT_hello,
    ):
        bpy.utils.unregister_class(cls)
