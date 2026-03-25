#!/usr/bin/env python3
"""Check internal markdown links in repository documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def should_skip(target: str) -> bool:
    if target.startswith(SKIP_PREFIXES):
        return True
    # Skip Windows drive paths and URI paths in docs.
    if re.match(r"^[A-Za-z]:[/\\]", target):
        return True
    return False


def normalize_target(path: Path, target: str, repo_root: Path) -> Path:
    clean_target = target.split("#", 1)[0].strip()
    if clean_target.startswith("/"):
        return repo_root / clean_target.lstrip("/")
    return (path.parent / clean_target).resolve()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    files = list(repo_root.rglob("*.md")) + list(repo_root.rglob("*.mdc"))
    errors: list[str] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        for _, target in MARKDOWN_LINK.findall(text):
            if should_skip(target):
                continue

            target_path = normalize_target(path, target, repo_root)
            if not target_path.exists():
                errors.append(f"{path}: broken link target '{target}'")

    if errors:
        print("Link check failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
