# SPDX-License-Identifier: MIT
"""Tests for optimization planning."""

from __future__ import annotations

from pathlib import Path

from blender_tools import optimize


def test_plan_optimization(tmp_path: Path) -> None:
    src = Path("examples/spaceship.blend")
    dst = tmp_path / "opt.blend"
    opts = optimize.OptimizeOptions(decimate=0.5, recalc_normals=True, pack_textures=True)
    plan = optimize.plan_optimization("meshes", src, dst, opts)
    assert "decimate" in plan.operations[0]
    assert "recalculate normals" in plan.operations[1]
