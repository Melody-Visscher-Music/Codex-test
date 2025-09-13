"""Tests for the cleanup unused data operator."""

import importlib
import types

from tests import test_stub_bpy  # noqa: F401
from addons.blender_tools.operators import OBJECT_OT_cleanup_unused_data


def test_cleanup_unused_data_default_types():
    bpy = importlib.import_module("bpy")
    used_mesh = types.SimpleNamespace(users=1)
    unused_mesh = types.SimpleNamespace(users=0)
    used_mat = types.SimpleNamespace(users=1)
    unused_mat = types.SimpleNamespace(users=0)
    unused_img = types.SimpleNamespace(users=0)
    bpy.data.meshes[:] = [used_mesh, unused_mesh]
    bpy.data.materials[:] = [used_mat, unused_mat]
    bpy.data.images[:] = [unused_img]

    op = OBJECT_OT_cleanup_unused_data()
    result = op.execute(None)

    assert result == {"FINISHED"}
    assert bpy.data.meshes == [used_mesh]
    assert bpy.data.materials == [used_mat]
    assert bpy.data.images == []
    assert op.reported[-1][1] == "Removed 3 unused data-blocks"


def test_cleanup_unused_data_respects_flags():
    bpy = importlib.import_module("bpy")
    unused_mesh = types.SimpleNamespace(users=0)
    unused_mat = types.SimpleNamespace(users=0)
    bpy.data.meshes[:] = [unused_mesh]
    bpy.data.materials[:] = [unused_mat]
    bpy.data.images[:] = []

    op = OBJECT_OT_cleanup_unused_data()
    op.remove_meshes = False
    result = op.execute(None)

    assert result == {"FINISHED"}
    assert bpy.data.meshes == [unused_mesh]
    assert bpy.data.materials == []
    assert bpy.data.images == []
    assert op.reported[-1][1] == "Removed 1 unused data-blocks"
