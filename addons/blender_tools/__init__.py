
"""Blender Tools add-on initialization."""

__version__ = "0.1.0"

bl_info = {
    "name": "Blender Tools",
    "description": "Example Blender add-on",
    "author": "Codex",
    "version": tuple(int(v) for v in __version__.split(".")),

bl_info = {
    "name": "Blender Tools",
main
    "blender": (4, 3, 2),
    "category": "Object",
}

bootstrap-empty-github-repo-for-blender-project

def register() -> None:
    """Register all add-on classes."""
=======
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
