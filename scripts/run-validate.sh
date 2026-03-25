#!/usr/bin/env bash
set -euo pipefail

# Persist command output as build artifacts while preserving exit codes.
mkdir -p artifacts/validate
python scripts/lint-frontmatter.py | tee artifacts/validate/lint-frontmatter.txt
python scripts/validate-index.py | tee artifacts/validate/validate-index.txt
python scripts/check-links.py | tee artifacts/validate/check-links.txt
