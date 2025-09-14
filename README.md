# Blender Scripting Toolkit

Utilities for developing Blender automation outside the Blender UI. The toolkit relies on [fake-bpy-module](https://github.com/nutti/fake-bpy-module) to simulate Blender's API so scripts can be linted and tested without launching Blender.

## Setup

```sh
set -euo pipefail
python -m pip install -r requirements.txt
```

## Usage

Batch export objects:

```python
from scripts import batch_export
batch_export(["Cube"], "out", ["FBX", "GLTF"], dry_run=True)
```

Optimize a mesh:

```python
from scripts import optimize_object
optimize_object(obj, decimate_ratio=0.25, triangulate=True, dry_run=True)
```

Create a Principled material:

```python
from scripts import create_principled_material
mat = create_principled_material("MyMat", (0.8, 0.2, 0.1, 1.0), emission_strength=2.0)
```

Animate location keyframes:

```python
from scripts import apply_location_keyframes
apply_location_keyframes(obj, [1, 10], [(0, 0, 0), (1, 2, 3)], dry_run=True)
```

## Development

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
- [Blender Manual – ShaderNodeBsdfPrincipled](https://docs.blender.org/api/current/bpy.types.ShaderNodeBsdfPrincipled.html)
- [Blender Manual – NLA Operators](https://docs.blender.org/api/current/bpy.ops.nla.html)
- [Blender Manual – Object Operators](https://docs.blender.org/api/current/bpy.ops.object.html)
- [fake-bpy-module README](https://github.com/nutti/fake-bpy-module)
