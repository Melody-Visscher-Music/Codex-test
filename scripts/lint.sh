#!/bin/sh
# SPDX-License-Identifier: MIT
set -e
poetry run ruff .
poetry run pydocstyle blender_tools tests
