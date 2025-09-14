# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""Simple Conventional Commit checker."""

from __future__ import annotations

import re
import sys

PATTERN = re.compile(r"^(feat|fix|chore|docs|style|refactor|test|perf|ci)(\([\w-]+\))?!?: .+")


def main(path: str) -> int:
    message = open(path, encoding="utf8").read().strip()
    if PATTERN.match(message):
        return 0
    print("Commit message does not follow Conventional Commits", file=sys.stderr)
    return 1


if __name__ == "__main__":  # pragma: no cover - script
    raise SystemExit(main(sys.argv[1]))
