#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GH_TOKEN:-}" || -z "${RUN_ID:-}" || -z "${HEAD_SHA:-}" ]]; then
  echo "Required environment variables are missing"
  echo "Expected: GH_TOKEN, RUN_ID, HEAD_SHA"
  exit 1
fi

mkdir -p artifacts

manifest_file="$(mktemp)"
python - <<'PY' > "${manifest_file}"
from pathlib import Path
import yaml

index_files = [
    Path("subagents/index.yaml"),
    Path("skills/index.yaml"),
    Path("prompts/index.yaml"),
]

selected = []
for index_file in index_files:
    data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
    for entry in data.get("entries", []):
        rel_path = str(entry.get("path", "")).strip()
        if not rel_path:
            continue
        domain_dir = index_file.parent
        candidate = domain_dir / rel_path
        if candidate.suffix == ".md" and candidate.exists():
            selected.append(str(candidate).replace("\\", "/"))

for path in sorted(set(selected)):
    print(path)
PY

if [[ ! -s "${manifest_file}" ]]; then
  echo "No markdown files referenced by index.yaml files were found"
  exit 1
fi

zip_file="artifacts/generated-markdown-run-${RUN_ID}.zip"
zip -q "${zip_file}" -@ < "${manifest_file}"

tag="generated-markdown-run-${RUN_ID}"
title="Generated markdown run ${RUN_ID}"
notes_file="$(mktemp)"
cat > "${notes_file}" <<EOF
Draft release with generated markdown files from workflow run ${RUN_ID}.
Source commit: ${HEAD_SHA}
EOF

gh release create "${tag}" "${zip_file}" --draft --title "${title}" --notes-file "${notes_file}" --target "${HEAD_SHA}"
