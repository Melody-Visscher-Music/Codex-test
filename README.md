# Blender Ultimate Scripting Suite

[![CI](https://github.com/blender-ultimate-scripting-suite/blender-ultimate-scripting-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/blender-ultimate-scripting-suite/blender-ultimate-scripting-suite/actions/workflows/ci.yml)

CLI utilities for planning Blender exports, optimizations and animation tasks without requiring a Blender runtime.

## Installation

```sh
./scripts/install.sh
```

## Usage

Examples:

```sh
blender-tools export glb --input examples/spaceship.blend --output build/spaceship.glb --triangulate --apply-modifiers --merge-by-distance 0.0001 --dry-run
blender-tools optimize meshes --input examples/spaceship.blend --output build/mesh.blend --decimate 0.5 --recalc-normals --pack-textures --dry-run
blender-tools animation bake --input examples/spaceship.blend --output build/anim.blend --fps 60 --strip-nla --key-reduce 0.05 --dry-run
blender-tools validate --dry-run
```

### CLI Help

<!-- CLI_HELP_START -->
```
usage: blender-tools [-h] {export,optimize,animation,validate} ...

positional arguments:
  {export,optimize,animation,validate}
    export              export assets
    optimize            optimize data
    animation           animation operations
    validate            run repository checks

options:
  -h, --help            show this help message and exit
```
<!-- CLI_HELP_END -->

## Validation without Blender

The project relies on [`fake-bpy-module`](https://pypi.org/project/fake-bpy-module-4.3/) and in-memory scene simulations to verify planner logic. This enables full testing in CI without invoking Blender.

## Architecture

```
+-----------------------------+
| blender_tools (package)     |
|  |-- export.py              |
|  |-- optimize.py            |
|  |-- animation.py           |
|  \-- scenesim/             |
|       |-- fake_scene.py     |
|       \-- adapters.py       |
+-----------------------------+
```

## Troubleshooting

- Ensure `python3` and `pip` are installed. If `pip` is missing, install via your package manager (`apt install python3-pip`).
- To regenerate documentation after modifying the CLI, run the Docs workflow or execute the snippet from `.github/workflows/docs.yml` locally.
- To resolve merge conflicts, run `./scripts/resolve-merge-conflicts.sh`.
- Update dependencies with `poetry update` followed by `poetry lock`.

## License

MIT

