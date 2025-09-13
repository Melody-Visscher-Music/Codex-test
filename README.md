# Blender Tools

Blender Tools is a collection of helpers for Blender 4.3.2 targeting game-ready workflows.

## Features

- **Optimize**: cleanup unused meshes, materials, and images; remove duplicate vertices; cleanup meshes; dedupe materials.
- **UV Tools**: smart unwrap and pack islands.
- **Materials**: create a PBR node template.
- **Baking**: quick texture bake presets.
- **Export**: Godot-friendly GLB exporter.
- **Animation**: push actions to NLA tracks.

## Installation

Copy the `addons/blender_tools` folder into your Blender add-ons directory or install the ZIP built from this repository.

## Development

```bash
pip install -r requirements-dev.txt
black .
pytest -q
```

## License

MIT
