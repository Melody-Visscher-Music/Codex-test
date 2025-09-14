# SPDX-License-Identifier: MIT
"""Optimization planning utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class OptimizeOptions:
    """Options for optimization planning."""

    decimate: float | None = None
    recalc_normals: bool = False
    pack_textures: bool = False


@dataclass
class OptimizePlan:
    """Representation of an optimization operation."""

    kind: str
    input_path: Path
    output_path: Path
    operations: list[str] = field(default_factory=list)


def plan_optimization(
    kind: str, input_path: Path, output_path: Path, options: OptimizeOptions
) -> OptimizePlan:
    """Generate an :class:`OptimizePlan` for the given data type."""
    if kind not in {"meshes", "materials", "scene"}:
        raise ValueError(f"Unsupported optimization kind: {kind}")  # pragma: no cover
    if not input_path.exists():
        raise FileNotFoundError(input_path)  # pragma: no cover
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ops: list[str] = []
    if options.decimate is not None:
        ops.append(f"decimate {options.decimate:.2f}")
    if options.recalc_normals:
        ops.append("recalculate normals")
    if options.pack_textures:
        ops.append("pack textures")

    return OptimizePlan(kind, input_path, output_path, ops)
