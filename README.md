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

## Install and use skills, subagents, and prompts

Artifacts here are plain Markdown with YAML frontmatter. The recommended install method is to run the repository install script. Manual copy remains fully supported.

### Recommended: install script (copy mode)

Run from the repository root:

```bash
# Linux/macOS or Windows (Git Bash)
bash scripts/install.sh
```

What the script does:

- Detects compatible client directories automatically (Cursor global/project, Claude Code, Gemini CLI, Copilot).
- Copies artifacts from `skills/`, `subagents/`, and `prompts/` into detected destinations.
- Prints frequent status messages in English for each step.
- Skips existing files by default and logs warnings; use `--overwrite` to replace files.
- Uses copy mode only (no symlink setup). Re-run the script whenever you want to update installed files.

### Get the files

- Clone this repository, or add it as a submodule in a project that should track versions of these assets.
- Browse `skills/`, `subagents/`, and `prompts/` and use the matching `index.yaml` to find entries.

### Skills (Cursor)

Cursor loads skills from a directory that contains `SKILL.md`:

- User-wide: `~/.cursor/skills/<skill-folder>/SKILL.md`
- Project: `.cursor/skills/<skill-folder>/SKILL.md`

Copy or adapt a file from `skills/<name>.md` into that layout. Cursor’s skill format expects YAML frontmatter with at least `name` and `description`; map from this repo (for example set `description` from `purpose` when you only have the catalog fields here). Other agents may use different paths or filenames—follow that product’s documentation and keep this repository as the canonical text.

### Manual install (alternative)

If you do not want to run the script, copy files manually from this repository into your tool-specific directories.
The existing guidance below remains valid for manual installation.

### Subagents

Subagent definitions live in `subagents/<name>.md`. Copy them into your project or leave them in a checkout of this repo, then reference the path from your agent setup (for example orchestration instructions or `AGENTS.md`) so dispatched runs can read the frontmatter contract.

### Prompts

Prompts live in `prompts/<name>.md`. Install them by copying into your prompt library, Cursor rules, or team docs, or reference the file directly in the client if it supports file context (for example `@path/to/prompt.md`).

### After install

Open the target path in your editor and confirm your tool discovers or invokes the asset. Run the validation scripts in this repo only when you change artifacts here before contributing.

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
