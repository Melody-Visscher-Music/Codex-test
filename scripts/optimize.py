"""Optimization helpers."""

from __future__ import annotations

try:
    import bpy
except ModuleNotFoundError:  # pragma: no cover
    bpy = None  # type: ignore


def decimate_object(
    obj, ratio: float, apply: bool = False, dry_run: bool = False
) -> float:
    """Apply a decimate modifier to *obj* with the given *ratio*."""
    if dry_run or bpy is None:
        print(f"[DRY RUN] Would decimate {getattr(obj, 'name', 'obj')} to {ratio}")
        return ratio
    modifier = obj.modifiers.new(name="Decimate", type="DECIMATE")
    modifier.ratio = ratio
    if apply:
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    return modifier.ratio
