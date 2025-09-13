#!/usr/bin/env python3
"""Apply automatic fixes for common issues."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True)


def ensure_blender_version() -> bool:
    """Ensure the add-on targets Blender 4.3.2."""
    init_file = ROOT / "addons" / "blender_tools.py"
    if not init_file.exists():
        return False
    text = init_file.read_text()
    new_text = re.sub(r'("blender":\s*)(\((?:\d+,\s*){2}\d+\))', r"\1(4, 3, 2)", text)
    if text != new_text:
        init_file.write_text(new_text)
        return True
    return False


def main() -> None:
    ensure_blender_version()
    run(["black", "."])
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True
    ).stdout.strip()
    if status:
        subprocess.run(
            ["git", "config", "user.name", "github-actions"], cwd=ROOT, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "github-actions@github.com"],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: apply auto fixes"], cwd=ROOT, check=True
        )


if __name__ == "__main__":
    main()
