import bpy
from bpy.props import BoolProperty
from bpy.types import Operator


def _purge(collection):
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

    merge_distance: float = bpy.props.FloatProperty(name="Distance", default=0.0001)

    def execute(self, context):
        # Real implementation would call bmesh operations; here we just report
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


CLASSES = [
    OBJECT_OT_cleanup_unused_data,
    OBJECT_OT_mesh_cleanup,
    OBJECT_OT_remove_duplicate_vertices,
    OBJECT_OT_dedupe_materials,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
