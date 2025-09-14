#!/bin/sh
# SPDX-License-Identifier: MIT
set -e
poetry run pytest --cov=blender_tools --cov-report=term-missing "$@"
