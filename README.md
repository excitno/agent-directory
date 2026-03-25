# agent-directory

Repository for managing reusable subagents, skills, and prompts for AI agent workflows.

## Repository purpose

This repository standardizes how agent assets are defined, validated, reviewed, and published.
It is optimized for Markdown/YAML-first authoring with automated quality checks in local and CI flows.

## Structure overview

- `subagents/`: subagent artifacts and `index.yaml`
- `skills/`: skill artifacts and `index.yaml`
- `prompts/`: prompt artifacts and `index.yaml`
- `templates/`: starter templates for new artifacts
- `schemas/`: metadata schema definitions
- `scripts/`: local validation scripts
- `docs/`: contribution and review guidance
- `.cursor/rules/`: persistent Cursor guidance for this repository
- `.github/workflows/`: CI quality gates

## Add a new subagent, skill, or prompt

1. Copy the relevant template from `templates/`.
2. Save the new artifact in the correct domain folder:
   - `subagents/<name>.md`
   - `skills/<name>.md`
   - `prompts/<name>.md`
3. Fill all required frontmatter fields.
4. Add an entry to the matching `index.yaml`.
5. Run validations locally:
   - `python scripts/lint-frontmatter.py`
   - `python scripts/validate-index.py`
   - `python scripts/check-links.py`
6. Open a pull request with focused, reviewable changes.
