# SPDX-License-Identifier: MIT
"""Tests for CLI entry points."""

from __future__ import annotations

from pathlib import Path

from blender_tools import cli


def test_export_dry_run(capfd, tmp_path: Path) -> None:
    out = tmp_path / "out.glb"
    cli.main(
        [
            "export",
            "glb",
            "--input",
            str(Path("examples/spaceship.blend")),
            "--output",
            str(out),
            "--triangulate",
            "--apply-modifiers",
            "--merge-by-distance",
            "0.01",
            "--dry-run",
        ]
    )
    captured = capfd.readouterr().out
    assert "Would export" in captured
    assert "glb" in captured


def test_validate_dry_run(capfd) -> None:
    cli.main(["validate", "--dry-run"])
    captured = capfd.readouterr().out
    assert "scripts/format.sh" in captured
