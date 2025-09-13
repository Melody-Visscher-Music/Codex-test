"""Blender Tools add-on initialization."""

__version__ = "0.1.0"

bl_info = {
    "name": "Blender Tools",
    "description": "Example Blender add-on",
    "author": "Codex",
    "version": tuple(int(v) for v in __version__.split(".")),
    "blender": (4, 3, 2),
    "category": "Object",
}


def register() -> None:
    """Register all add-on classes."""
    from . import operators

    operators.register()


def unregister() -> None:
    """Unregister all add-on classes."""
    from . import operators

    operators.unregister()

