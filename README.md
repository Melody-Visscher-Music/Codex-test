# Blender Tools

bootstrap-empty-github-repo-for-blender-project
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

A Blender 4.3.2 addon project.

 bootstrap-empty-github-repo-for-blender-project
## Add-on Features

- Provides `object.hello` operator that logs "Hello World" to the Info log.
- Includes `object.cleanup_unused_data` operator to remove unused meshes, materials, and images with configurable data-type toggles.
- Supplies `object.remove_duplicate_vertices` operator that collapses duplicate vertices across all meshes.

 main
 main
## Development

```bash
pip install -r requirements-dev.txt
black .
pytest -q
```

 bootstrap-empty-github-repo-for-blender-project
Pull requests are checked and can be auto-merged by the **Auto PR Merge** workflow.

## License

MIT
## Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.

## Release

Semantic-release runs on the `main` branch and publishes new versions.
main
