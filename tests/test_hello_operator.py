"""Tests for the hello operator."""

from tests import test_stub_bpy  # noqa: F401

from addons.blender_tools.operators import OBJECT_OT_hello


def test_operator_execute():
    op = OBJECT_OT_hello()
    result = op.execute(None)
    assert result == {"FINISHED"}
    assert op.reported[0][1] == "Hello World"
