"""Animation helpers."""

from __future__ import annotations
from typing import Iterable, Sequence, List, Tuple

try:
    import bpy
except ModuleNotFoundError:  # pragma: no cover
    bpy = None  # type: ignore


def apply_location_keyframes(
    obj,
    frames: Iterable[int],
    locations: Iterable[Sequence[float]],
    dry_run: bool = False,
) -> List[Tuple[int, Sequence[float]]]:
    """Insert location keyframes for *obj*.

    Returns a list of ``(frame, location)`` tuples."""
    data = list(zip(frames, locations))
    if dry_run or bpy is None:
        return data
    for frame, loc in data:
        obj.location = loc
        obj.keyframe_insert(data_path="location", frame=frame)
    return data
