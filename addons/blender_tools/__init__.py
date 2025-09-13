"""Blender Tools Add-on"""

__version__ = "0.1.0"

bl_info = {
    "name": "Blender Tools",
    "blender": (4, 3, 2),
    "category": "Object",
}

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


def register() -> None:
    for module in MODULES:
        if hasattr(module, "register"):
            module.register()


def unregister() -> None:
    for module in reversed(MODULES):
        if hasattr(module, "unregister"):
            module.unregister()
