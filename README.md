# Blender Scripting Toolkit

Utilities for developing Blender automation outside the Blender UI. The toolkit relies on [fake-bpy-module](https://github.com/nutti/fake-bpy-module) to simulate Blender's API so scripts can be linted and tested without launching Blender.

## Setup

```sh
set -euo pipefail
python -m pip install -r requirements.txt
```

## Usage

Example: export selected objects as FBX with a safety dry run.

```python
from scripts import export
export.export_fbx(["Cube"], "out.fbx", dry_run=True)
```

Run tests and linters before committing:

```sh
set -euo pipefail
pre-commit run --files $(git ls-files '*.py')
pytest
```

## References

- [Blender Manual – Export Scene Operators](https://docs.blender.org/api/current/bpy.ops.export_scene.html)
- [fake-bpy-module README](https://github.com/nutti/fake-bpy-module)
