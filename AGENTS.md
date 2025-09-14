# Project Guidelines
- Use Python 3.11 or newer.
- Format code with Black and ensure Flake8 passes.
- Run `pre-commit run --files <files>` before committing.
- Execute the full test suite via `pytest`.
- Wrap potentially destructive Blender operations with a `dry_run` flag.
- Consolidated utilities live in `scripts/blender_toolkit.py`.
