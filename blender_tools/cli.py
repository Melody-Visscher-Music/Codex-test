# SPDX-License-Identifier: MIT
"""Command line interface for blender_tools.

This module exposes the ``blender-tools`` executable which plans operations
without requiring a Blender runtime.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Sequence

from rich.console import Console


def _ensure_path(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")
    return path


def _export_command(args: argparse.Namespace, console: Console) -> int:
    from . import export as export_mod

    options = export_mod.ExportOptions(
        triangulate=args.triangulate,
        apply_modifiers=args.apply_modifiers,
        merge_by_distance=args.merge_by_distance,
    )
    plan = export_mod.plan_export(args.format, _ensure_path(args.input), args.output, options)
    console.print(f"Would export {plan.input_path} to {plan.output_path} as {plan.format}")
    if args.dry_run:
        return 0
    console.print("Dry run only; real export requires Blender integration.")  # pragma: no cover
    return 0  # pragma: no cover


def _optimize_command(args: argparse.Namespace, console: Console) -> int:
    from . import optimize as optimize_mod

    options = optimize_mod.OptimizeOptions(
        decimate=args.decimate,
        recalc_normals=args.recalc_normals,
        pack_textures=args.pack_textures,
    )
    plan = optimize_mod.plan_optimization(args.kind, _ensure_path(args.input), args.output, options)
    console.print(f"Optimization plan: {plan.operations}")
    if args.dry_run:
        return 0
    console.print("Dry run only; no changes made.")  # pragma: no cover
    return 0  # pragma: no cover


def _animation_command(args: argparse.Namespace, console: Console) -> int:
    from . import animation as animation_mod

    options = animation_mod.AnimationOptions(
        fps=args.fps,
        strip_nla=args.strip_nla,
        key_reduce=args.key_reduce,
    )
    plan = animation_mod.plan_animation(args.action, _ensure_path(args.input), args.output, options)
    console.print(f"Animation plan: {plan.operations}")
    if args.dry_run:
        return 0
    console.print("Dry run only; no changes made.")  # pragma: no cover
    return 0  # pragma: no cover


def _validate_command(args: argparse.Namespace, console: Console) -> int:
    commands = [
        ["./scripts/format.sh"],
        ["./scripts/lint.sh"],
        ["./scripts/typecheck.sh"],
        ["./scripts/test.sh"],
    ]
    for cmd in commands:
        console.print("Would run", " ".join(cmd))
    if args.dry_run:
        return 0
    for cmd in commands:  # pragma: no cover
        subprocess.run(cmd, check=True)  # pragma: no cover
    return 0  # pragma: no cover


def build_parser() -> argparse.ArgumentParser:
    """Create the top-level argument parser."""
    parser = argparse.ArgumentParser(prog="blender-tools")
    sub = parser.add_subparsers(dest="command", required=True)

    # export
    p_export = sub.add_parser("export", help="export assets")
    export_sub = p_export.add_subparsers(dest="format", required=True)
    for fmt in ("glb", "fbx", "obj"):
        f_parser = export_sub.add_parser(fmt)
        f_parser.add_argument("--input", type=Path, required=True)
        f_parser.add_argument("--output", type=Path, required=True)
        f_parser.add_argument("--triangulate", action="store_true")
        f_parser.add_argument("--apply-modifiers", action="store_true")
        f_parser.add_argument("--merge-by-distance", type=float)
        f_parser.add_argument("--dry-run", action="store_true")
        f_parser.set_defaults(func=_export_command, format=fmt)

    # optimize
    p_opt = sub.add_parser("optimize", help="optimize data")
    opt_sub = p_opt.add_subparsers(dest="kind", required=True)
    for kind in ("meshes", "materials", "scene"):
        o_parser = opt_sub.add_parser(kind)
        o_parser.add_argument("--input", type=Path, required=True)
        o_parser.add_argument("--output", type=Path, required=True)
        o_parser.add_argument("--decimate", type=float)
        o_parser.add_argument("--recalc-normals", action="store_true")
        o_parser.add_argument("--pack-textures", action="store_true")
        o_parser.add_argument("--dry-run", action="store_true")
        o_parser.set_defaults(func=_optimize_command, kind=kind)

    # animation
    p_anim = sub.add_parser("animation", help="animation operations")
    anim_sub = p_anim.add_subparsers(dest="action", required=True)
    for action in ("bake", "retarget", "clean"):
        a_parser = anim_sub.add_parser(action)
        a_parser.add_argument("--input", type=Path, required=True)
        a_parser.add_argument("--output", type=Path, required=True)
        a_parser.add_argument("--fps", type=int, default=24)
        a_parser.add_argument("--strip-nla", action="store_true")
        a_parser.add_argument("--key-reduce", type=float)
        a_parser.add_argument("--dry-run", action="store_true")
        a_parser.set_defaults(func=_animation_command, action=action)

    # validate
    p_val = sub.add_parser("validate", help="run repository checks")
    p_val.add_argument("--dry-run", action="store_true")
    p_val.set_defaults(func=_validate_command)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Optional sequence of arguments.

    Returns:
        Exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    console = Console()
    func = args.func
    return func(args, console)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    raise SystemExit(main())
