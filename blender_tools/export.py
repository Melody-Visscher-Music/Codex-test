# SPDX-License-Identifier: MIT
"""Export planning utilities.

Pure-Python helpers to validate export options and outline operations that
would be performed in Blender.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExportOptions:
    """Options controlling export behaviour."""

    triangulate: bool = False
    apply_modifiers: bool = False
    merge_by_distance: float | None = None


@dataclass
class ExportPlan:
    """Structured representation of an export operation."""

    format: str
    input_path: Path
    output_path: Path
    options: ExportOptions


def plan_export(
    fmt: str, input_path: Path, output_path: Path, options: ExportOptions
) -> ExportPlan:
    """Validate arguments and return an :class:`ExportPlan`.

    Args:
        fmt: One of ``glb``, ``fbx`` or ``obj``.
        input_path: Source Blender file.
        output_path: Destination file.
        options: Export options.

    Returns:
        The planned export.

    Raises:
        FileNotFoundError: If ``input_path`` does not exist.
        ValueError: If ``fmt`` is unsupported.
    """
    if fmt not in {"glb", "fbx", "obj"}:
        raise ValueError(f"Unsupported format: {fmt}")  # pragma: no cover
    if not input_path.exists():
        raise FileNotFoundError(input_path)  # pragma: no cover
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return ExportPlan(fmt, input_path, output_path, options)
