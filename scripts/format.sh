#!/bin/sh
# SPDX-License-Identifier: MIT
set -e
if [ "$FIX" = "1" ]; then
    poetry run black .
    poetry run isort .
else
    poetry run black --check .
    poetry run isort --check-only .
fi
