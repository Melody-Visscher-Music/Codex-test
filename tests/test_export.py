# SPDX-License-Identifier: MIT
"""Tests for export planning."""

from __future__ import annotations

from pathlib import Path

import pytest

from blender_tools import export


def test_plan_export(tmp_path: Path) -> None:
    src = Path("examples/spaceship.blend")
    dst = tmp_path / "out.fbx"
    opts = export.ExportOptions(triangulate=True, apply_modifiers=True, merge_by_distance=0.1)
    plan = export.plan_export("fbx", src, dst, opts)
    assert plan.format == "fbx"
    assert plan.options.triangulate


def test_plan_export_unknown_format(tmp_path: Path) -> None:
    src = tmp_path / "in.blend"
    src.write_text("dummy")
    with pytest.raises(ValueError):
        export.plan_export("abc", src, tmp_path / "o.obj", export.ExportOptions())
