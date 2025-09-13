"""Tests for the remove duplicate vertices operator."""

import types

import bpy
from tests import test_stub_bpy  # noqa: F401

from addons.blender_tools.operators import OBJECT_OT_remove_duplicate_vertices


def test_remove_duplicate_vertices_operator():
    mesh = types.SimpleNamespace(vertices=[(0, 0, 0), (0, 0, 0), (1, 1, 1)])
    bpy.data.meshes = [mesh]

    op = OBJECT_OT_remove_duplicate_vertices()
    result = op.execute(None)

    assert result == {"FINISHED"}
    assert mesh.vertices == [(0, 0, 0), (1, 1, 1)]
    assert op.reported[0][1] == "Removed 1 duplicate vertices"
