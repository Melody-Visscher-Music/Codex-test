# SPDX-License-Identifier: MIT
"""Animation planning utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AnimationOptions:
    """Options for animation planning."""

    fps: int = 24
    strip_nla: bool = False
    key_reduce: float | None = None


@dataclass
class AnimationPlan:
    """Representation of an animation operation."""

    action: str
    input_path: Path
    output_path: Path
    operations: list[str] = field(default_factory=list)


def plan_animation(
    action: str, input_path: Path, output_path: Path, options: AnimationOptions
) -> AnimationPlan:
    """Create a plan for animation operations."""
    if action not in {"bake", "retarget", "clean"}:
        raise ValueError(f"Unsupported action: {action}")  # pragma: no cover
    if not input_path.exists():
        raise FileNotFoundError(input_path)  # pragma: no cover
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ops: list[str] = [f"fps={options.fps}"]
    if options.strip_nla:
        ops.append("strip NLA")
    if options.key_reduce is not None:
        ops.append(f"key reduce {options.key_reduce:.3f}")

    ops.insert(0, action)
    return AnimationPlan(action, input_path, output_path, ops)
