 bootstrap-empty-github-repo-for-blender-project
"""Blender Tools Add-on"""

"""Blender Tools add-on initialization."""
 main

__version__ = "0.1.0"

bl_info = {
    "name": "Blender Tools",
bootstrap-empty-github-repo-for-blender-project
    "description": "Example Blender add-on",
    "author": "Codex",
    "version": tuple(int(v) for v in __version__.split(".")),

bl_info = {
    "name": "Blender Tools",
main
 main
    "blender": (4, 3, 2),
    "category": "Object",
}

 bootstrap-empty-github-repo-for-blender-project
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

bootstrap-empty-github-repo-for-blender-project

def register() -> None:
    """Register all add-on classes."""

__version__ = "0.1.0"


def register():
main
    from . import operators

    operators.register()


 bootstrap-empty-github-repo-for-blender-project
def unregister() -> None:
    """Unregister all add-on classes."""
    from . import operators

    operators.unregister()


def unregister():
    from . import operators

    operators.unregister()
 main
 main
