#!/bin/sh
# SPDX-License-Identifier: MIT
set -e

PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
    echo "python3 not found" >&2
    exit 1
fi
"$PY" - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit('Python >=3.11 required')
PY

if ! command -v poetry >/dev/null 2>&1; then
    curl -sSL https://install.python-poetry.org | "$PY" -
    export PATH="$HOME/.local/bin:$PATH"
fi

poetry install --no-interaction --no-ansi
poetry run pre-commit install --install-hooks

git config rerere.enabled true

echo "Installed. Try: blender-tools --help"
