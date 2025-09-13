import importlib

from tests import test_stub_bpy  # noqa: F401


def test_register_unregister():
    addon = importlib.import_module("addons.blender_tools")
    assert hasattr(addon, "register")
    assert hasattr(addon, "unregister")
    addon.register()
    addon.unregister()
