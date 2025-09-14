#!/bin/sh
# SPDX-License-Identifier: MIT
set -e
poetry run mypy blender_tools tests
