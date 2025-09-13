"""Tests for optimization.cleanup_unused_data."""

import importlib
import types

from tests import test_stub_bpy  # noqa: F401
from addons.blender_tools import optimization


def test_cleanup_specific_types():
    bpy = importlib.import_module("bpy")
    unused_mesh = types.SimpleNamespace(users=0)
    unused_image = types.SimpleNamespace(users=0)
    bpy.data.meshes[:] = [unused_mesh]
    bpy.data.images[:] = [unused_image]

    removed = optimization.cleanup_unused_data(["images"])

    assert removed == 1
    assert bpy.data.meshes == [unused_mesh]
    assert bpy.data.images == []
