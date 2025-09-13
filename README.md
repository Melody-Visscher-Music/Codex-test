# Blender Tools

A Blender 4.3.2 addon project.

## Add-on Features

- Provides `object.hello` operator that logs "Hello World" to the Info log.
- Includes `object.cleanup_unused_data` operator to remove unused meshes, materials, and images with configurable data-type toggles.
- Supplies `object.remove_duplicate_vertices` operator that collapses duplicate vertices across all meshes.

## Development

```bash
pip install -r requirements-dev.txt
black .
pytest -q
```

## Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.

## Release

Semantic-release runs on the `main` branch and publishes new versions.
