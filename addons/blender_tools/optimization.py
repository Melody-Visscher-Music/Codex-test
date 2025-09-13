"""Utility functions for optimizing Blender data-blocks."""

from __future__ import annotations

import bpy
from typing import Iterable, Optional


def _remove_unused(datablocks: Iterable) -> int:
    removed = 0
    for block in list(datablocks):
        if getattr(block, "users", 0) == 0:
            datablocks.remove(block)
            removed += 1
    return removed


def cleanup_unused_data(types: Optional[Iterable[str]] = None) -> int:
    """Remove unused data-blocks for given ``types``.

    Parameters
    ----------
    types: Iterable[str] or None
        Names of collections on ``bpy.data`` to clean. When ``None``,
        ``meshes``, ``materials`` and ``images`` are processed.

    Returns
    -------
    int
        Number of removed data-blocks.
    """
    data = bpy.data
    total = 0
    if types is None:
        types = ("meshes", "materials", "images")
    for attr in types:
        collection = getattr(data, attr, [])
        total += _remove_unused(collection)
    return total


def remove_duplicate_vertices(mesh) -> int:
    """Remove duplicate vertices from ``mesh``.

    Parameters
    ----------
    mesh: Any
        Mesh-like object containing a ``vertices`` sequence.

    Returns
    -------
    int
        Number of removed vertices.
    """

    unique = []
    seen = set()
    removed = 0
    for vert in getattr(mesh, "vertices", []):
        key = tuple(vert)
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        unique.append(vert)
    mesh.vertices = unique
    return removed


def remove_duplicate_vertices_from_meshes(
    meshes: Optional[Iterable] = None,
) -> int:
    """Remove duplicate vertices from all meshes.

    Parameters
    ----------
    meshes: Iterable or None
        Sequence of mesh objects. When ``None``, ``bpy.data.meshes`` is used.

    Returns
    -------
    int
        Total number of removed vertices.
    """

    if meshes is None:
        meshes = bpy.data.meshes
    total = 0
    for mesh in meshes:
        total += remove_duplicate_vertices(mesh)
    return total
