#!/usr/bin/env python3
"""Validate index.yaml files for subagents, skills, and prompts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_index_entries(text: str) -> tuple[list[dict[str, str]], list[str]]:
    entries: list[dict[str, str]] = []
    errors: list[str] = []
    current: dict[str, str] | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if line.startswith("entries:"):
            continue

        if line.startswith("- "):
            if current:
                entries.append(current)
            current = {}
            remainder = line[2:].strip()
            if remainder:
                if ":" not in remainder:
                    errors.append(f"invalid inline entry line '{line}'")
                    continue
                key, value = remainder.split(":", 1)
                current[key.strip()] = value.strip()
            continue

        if line.startswith("  ") and ":" in line and current is not None:
            key, value = line.strip().split(":", 1)
            current[key.strip()] = value.strip()
            continue

        errors.append(f"unsupported line format '{line}'")

    if current:
        entries.append(current)

    return entries, errors


def validate_index_file(path: Path, section: str) -> list[str]:
    if not path.exists():
        return [f"{path}: file is missing"]

    text = path.read_text(encoding="utf-8")
    entries, parse_errors = parse_index_entries(text)
    errors = [f"{path}: {err}" for err in parse_errors]
    ids: dict[str, int] = {}

    for idx, entry in enumerate(entries):
        context = f"{path}: entry[{idx}]"
        for key in ("id", "path", "category", "version", "owner", "status"):
            if key not in entry or not entry[key]:
                errors.append(f"{context} missing '{key}'")

        entry_id = entry.get("id", "")
        if entry_id and not ID_PATTERN.match(entry_id):
            errors.append(f"{context} invalid id '{entry_id}'")

        if entry_id:
            ids[entry_id] = ids.get(entry_id, 0) + 1

        rel_path = entry.get("path")
        if rel_path:
            artifact_path = path.parent / rel_path
            if artifact_path.suffix != ".md":
                errors.append(f"{context} path must target a markdown file: '{rel_path}'")
            if not artifact_path.exists():
                errors.append(f"{context} missing referenced file '{rel_path}'")
            else:
                # Validate that referenced files stay in the expected domain folder.
                expected_root = path.parent.resolve()
                if expected_root not in artifact_path.resolve().parents:
                    errors.append(f"{context} path escapes '{section}' directory")

    for entry_id, count in ids.items():
        if count > 1:
            errors.append(f"{path}: duplicate id '{entry_id}' in index entries")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    sections = ("subagents", "skills", "prompts")
    all_errors: list[str] = []

    for section in sections:
        index_path = root / section / "index.yaml"
        all_errors.extend(validate_index_file(index_path, section))

    if all_errors:
        print("Index validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Index validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
