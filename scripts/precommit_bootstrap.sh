#!/bin/sh
# SPDX-License-Identifier: MIT
set -e
poetry run pre-commit install --install-hooks -t pre-commit -t commit-msg
