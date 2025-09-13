# isort: skip_file
from tests import test_stub_bpy  # noqa: F401
import types

import bpy

import addons.blender_tools as bt
from addons.blender_tools.animation import operators as anim_ops
from addons.blender_tools.baking import operators as bake_ops
from addons.blender_tools.exporter import operators as export_ops
from addons.blender_tools.materials import operators as mat_ops
from addons.blender_tools.optimize import operators as opt_ops
from addons.blender_tools.uv import operators as uv_ops


def setup_module(module):
    bt.register()


def teardown_module(module):
    bt.unregister()


def test_optimize_cleanup_unused_data():
    mesh = types.SimpleNamespace(name="Mesh", users=0)
    mat = types.SimpleNamespace(name="Mat", users=0)
    img = types.SimpleNamespace(name="Img", users=0)
    bpy.data.meshes.append(mesh)
    bpy.data.materials.append(mat)
    bpy.data.images.append(img)
    op = opt_ops.OBJECT_OT_cleanup_unused_data()
    op.remove_materials = False
    op.remove_images = False
    assert op.execute(bpy.context) == {"FINISHED"}
    assert mesh not in bpy.data.meshes
    assert mat in bpy.data.materials
    assert img in bpy.data.images
    bpy.data.materials.clear()
    bpy.data.images.clear()


def test_optimize_remove_duplicate_vertices():
    mesh = types.SimpleNamespace(vertices=[(0, 0, 0), (0, 0, 0), (1, 0, 0)])
    bpy.context.object = types.SimpleNamespace(data=mesh)
    op = opt_ops.OBJECT_OT_remove_duplicate_vertices()
    assert op.execute(bpy.context) == {"FINISHED"}
    assert len(mesh.vertices) == 2


def test_uv_auto():
    op = uv_ops.UV_OT_auto_uv()
    assert op.execute(bpy.context) == {"FINISHED"}


def test_material_pbr():
    op = mat_ops.MATERIAL_OT_create_pbr_template()
    assert op.execute(bpy.context) == {"FINISHED"}


def test_bake_preset():
    op = bake_ops.OBJECT_OT_bake_preset()
    assert op.execute(bpy.context) == {"FINISHED"}


def test_export_glb():
    op = export_ops.EXPORT_SCENE_OT_godot_glb()
    assert op.execute(bpy.context) == {"FINISHED"}


def test_animation_push():
    op = anim_ops.OBJECT_OT_push_action_to_nla()
    assert op.execute(bpy.context) == {"FINISHED"}
