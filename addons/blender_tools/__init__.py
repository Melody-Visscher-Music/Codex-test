"""Blender Tools Add-on"""

bl_info = {
    "name": "Blender Tools",
    "blender": (4, 3, 2),
    "category": "Object",
}

__version__ = "1.0.0"

from .animation import operators as anim_ops
from .baking import operators as baking_ops
from .core import prefs
from .exporter import operators as export_ops
from .materials import operators as material_ops
from .optimize import operators as optimize_ops
from .ui import panel
from .uv import operators as uv_ops

MODULES = [
    prefs,
    optimize_ops,
    uv_ops,
    material_ops,
    baking_ops,
    export_ops,
    anim_ops,
    panel,
]


def register():
    for module in MODULES:
        if hasattr(module, "register"):
            module.register()


def unregister():
    for module in reversed(MODULES):
        if hasattr(module, "unregister"):
            module.unregister()
