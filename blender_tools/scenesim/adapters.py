# SPDX-License-Identifier: MIT
"""Adapters resolving the execution environment."""

from __future__ import annotations

import importlib
from typing import Any

from .fake_scene import Scene, create_demo_scene


def get_bpy() -> Any | None:
    """Attempt to import ``bpy`` lazily.

    Returns:
        The ``bpy`` module if importable, otherwise ``None``.
    """
    try:
        bpy = importlib.import_module("bpy")
        if getattr(getattr(bpy, "context", None), "scene", None) is None:
            return None
        return bpy
    except Exception:  # pragma: no cover - import failure path
        try:
            importlib.import_module("fake_bpy_module")  # pragma: no cover
        except Exception:  # pragma: no cover
            pass
        return None


def get_scene() -> Scene:
    """Return the active scene or a simulated one."""
    bpy = get_bpy()
    if bpy is not None:
        return bpy.context.scene  # pragma: no cover
    return create_demo_scene()
