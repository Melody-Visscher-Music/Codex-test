# SPDX-License-Identifier: MIT
"""Tests for animation planning."""

from __future__ import annotations

from pathlib import Path

from blender_tools import animation
from blender_tools.scenesim import adapters


def test_plan_animation(tmp_path: Path) -> None:
    src = Path("examples/spaceship.blend")
    dst = tmp_path / "anim.blend"
    opts = animation.AnimationOptions(fps=30, strip_nla=True, key_reduce=0.1)
    plan = animation.plan_animation("bake", src, dst, opts)
    assert plan.operations[0] == "bake"
    assert "fps=30" in plan.operations[1]


def test_get_scene_returns_demo() -> None:
    scene = adapters.get_scene()
    assert scene.objects
