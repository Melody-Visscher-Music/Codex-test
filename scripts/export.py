"""Export utilities using Blender's API."""

from __future__ import annotations

from typing import Iterable

try:
    import bpy
except ModuleNotFoundError:  # pragma: no cover
    bpy = None  # type: ignore


def _select_objects(names: Iterable[str]) -> None:
    for obj in bpy.data.objects:
        obj.select_set(obj.name in names)


def export_fbx(objects: Iterable[str], filepath: str, dry_run: bool = False) -> str:
    """Export objects to an FBX file."""
    if dry_run or bpy is None:
        print(f"[DRY RUN] Would export {list(objects)} to {filepath}")
        return filepath
    _select_objects(objects)
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True)
    return filepath


def export_gltf(objects: Iterable[str], filepath: str, dry_run: bool = False) -> str:
    """Export objects to a GLTF file."""
    if dry_run or bpy is None:
        print(f"[DRY RUN] Would export {list(objects)} to {filepath}")
        return filepath
    _select_objects(objects)
    bpy.ops.export_scene.gltf(filepath=filepath, export_selected=True)
    return filepath
