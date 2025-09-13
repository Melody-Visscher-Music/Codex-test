bl_info = {
    "name": "Blender Tools",
    "blender": (4, 3, 2),
    "category": "Object",
}

__version__ = "0.1.0"


def register():
    from . import operators

    operators.register()


def unregister():
    from . import operators

    operators.unregister()
