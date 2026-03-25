#!/usr/bin/env python3
"""Validate frontmatter blocks in subagents, skills, and prompts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "subagents": {
        "id",
        "name",
        "version",
        "owner",
        "status",
        "tags",
        "purpose",
        "input_contract",
        "output_contract",
        "constraints",
        "security",
        "error_handling",
    },
    "skills": {
        "id",
        "name",
        "version",
        "owner",
        "status",
        "tags",
        "purpose",
        "prerequisites",
        "input_contract",
        "output_contract",
        "constraints",
        "security",
        "error_handling",
    },
    "prompts": {
        "id",
        "name",
        "version",
        "owner",
        "status",
        "tags",
        "purpose",
        "prompt_type",
        "input_contract",
        "output_contract",
        "constraints",
        "security",
        "error_handling",
    },
}

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")
STATUS_VALUES = {"draft", "active", "deprecated"}
PROMPT_TYPES = {"system", "user", "assistant", "workflow"}


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening frontmatter delimiter ('---')"]

    end_idx = next((idx for idx, line in enumerate(lines[1:], start=1) if line.strip() == "---"), None)
    if end_idx is None:
        return {}, ["missing closing frontmatter delimiter ('---')"]

    data: dict[str, str] = {}
    errors: list[str] = []
    list_indent_key = None
    block_scalar_key = None

    for raw_line in lines[1:end_idx]:
        line = raw_line.rstrip()
        if not line.strip():
            continue

        if block_scalar_key is not None:
            # YAML block scalars continue on indented lines.
            if raw_line.startswith(" ") or raw_line.startswith("\t"):
                continue
            block_scalar_key = None

        # Handle list items under the latest list key (for tags/prerequisites/constraints).
        if line.lstrip().startswith("- "):
            if list_indent_key is None:
                errors.append(f"list item without a parent key: '{line.strip()}'")
            continue

        if ":" not in line:
            errors.append(f"invalid frontmatter line: '{line}'")
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        data[key] = value
        list_indent_key = key if value == "" else None
        block_scalar_key = key if value in {">", "|", ">-", "|-"} else None

    return data, errors


def collect_markdown_files(root: Path, section: str) -> list[Path]:
    base = root / section
    if not base.exists():
        return []
    return sorted(path for path in base.rglob("*.md") if path.name != "index.md")


def validate_file(path: Path, section: str) -> tuple[list[str], str | None]:
    text = path.read_text(encoding="utf-8")
    data, errors = parse_frontmatter(text)
    field_errors: list[str] = []

    if errors:
        return [f"{path}: {err}" for err in errors], None

    missing = REQUIRED_FIELDS[section] - set(data)
    for key in sorted(missing):
        field_errors.append(f"{path}: missing required frontmatter field '{key}'")

    file_id = data.get("id")
    if file_id and not ID_PATTERN.match(file_id):
        field_errors.append(f"{path}: invalid id '{file_id}' (must be snake-safe kebab-case)")

    version = data.get("version")
    if version and not VERSION_PATTERN.match(version):
        field_errors.append(f"{path}: invalid version '{version}' (expected vMAJOR.MINOR.PATCH)")

    status = data.get("status")
    if status and status not in STATUS_VALUES:
        field_errors.append(f"{path}: invalid status '{status}'")

    if section == "prompts":
        prompt_type = data.get("prompt_type")
        if prompt_type and prompt_type not in PROMPT_TYPES:
            field_errors.append(f"{path}: invalid prompt_type '{prompt_type}'")

    return field_errors, file_id


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    all_errors: list[str] = []
    ids: dict[str, Path] = {}

    for section in ("subagents", "skills", "prompts"):
        for md_file in collect_markdown_files(root, section):
            file_errors, file_id = validate_file(md_file, section)
            all_errors.extend(file_errors)
            if not file_id:
                continue
            previous = ids.get(file_id)
            if previous is not None:
                all_errors.append(f"duplicate id '{file_id}' in {previous} and {md_file}")
            else:
                ids[file_id] = md_file

    if all_errors:
        print("Frontmatter lint failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Frontmatter lint passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
