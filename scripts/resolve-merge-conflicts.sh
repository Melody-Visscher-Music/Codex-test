#!/bin/sh
# SPDX-License-Identifier: MIT
set -e
if git grep -l '^<<<<<<< ' -- */* >/dev/null 2>&1; then
    echo 'Conflict markers detected. Resolve conflicts before continuing.' >&2
    exit 1
fi
./scripts/format.sh
./scripts/lint.sh
./scripts/typecheck.sh
./scripts/test.sh
