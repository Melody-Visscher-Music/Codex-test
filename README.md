# Blender Tools

A Blender 4.3.2 addon project.

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
