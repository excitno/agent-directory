# Agent instructions – agent-directory

This repository is a **catalog** of reusable subagents, skills, and prompts. Keep content modular, discoverable, and aligned with schemas and CI.

## Map

| Area | Contents |
|------|----------|
| `subagents/` | Subagent definitions and `index.yaml` |
| `skills/` | Skills and `index.yaml` |
| `prompts/` | Prompts and `index.yaml` |
| `templates/` | Starter templates for new artifacts |
| `schemas/` | JSON Schema for frontmatter (`*.schema.yaml`) |
| `scripts/` | `lint-frontmatter.py`, `validate-index.py`, `check-links.py` |
| `docs/` | Contribution and process notes |
| `.cursor/rules/` | Cursor rules for this repository (read when unsure) |

## Subagents shipped in `subagents/` (default set)

Use `subagents/index.yaml` as the source of truth for paths and catalog metadata. Definitions are in the files below; full contracts are in YAML frontmatter plus the Markdown body.

| `id` | File | Name (frontmatter) | Purpose (summary) |
|------|------|-------------------|-------------------|
| `example-subagent-id` | `subagents/example-subagent.md` | Example Subagent | Execute focused research and execution tasks with a predictable output contract. |

When you add or remove a subagent, update **`subagents/index.yaml`** and **this table** so they stay aligned.

## Lookup

- Use the domain-specific `index.yaml` under `subagents/`, `skills/`, or `prompts/` for `id`, `path`, tags, and status.
- Each artifact’s contract lives in YAML frontmatter at the top of its `.md` file.

## Adding or changing an artifact

1. Copy the relevant template from `templates/`.
2. Add a file in the correct folder (`subagents/<name>.md`, etc.) using the same naming style as templates and existing files (kebab-case). Use **kebab-case** for service/app names in prose where applicable (see `.cursor/rules`).
3. Complete all required frontmatter fields per schema: `id` (kebab-case), `name`, `version`, `owner`, `status`, `tags`, `purpose`, `input_contract`, `output_contract`, `constraints`, `security`, `error_handling`.
4. Add an entry to the matching `index.yaml`.
5. Run validation locally before opening a PR:

   ```bash
   python scripts/lint-frontmatter.py
   python scripts/validate-index.py
   python scripts/check-links.py
   ```

6. Keep PRs **focused** (target on the order of 500 changed lines or fewer).

## Content expectations (short)

- State **purpose**, **inputs**, **outputs**, and **constraints** clearly. Document security and error handling where relevant.
- Do not add unnecessary READMEs that only summarize completed work unless explicitly requested.
- No comments inside JSON files.
- No scope creep beyond what the task asks for.

## Using subagents from this repository

Cursor does **not** auto-load these files as subagents. To apply a definition:

- Attach it as context (e.g. `@subagents/<name>.md`), or
- Copy it into another project and reference the path from that project’s `AGENTS.md` / orchestration.

This `AGENTS.md` applies to work **inside agent-directory**; other repos may use their own `AGENTS.md` at their root.
