# Contributing

## Scope

Contribute only subagents, skills, prompts, schemas, templates, scripts, and governance docs relevant to this repository.

## Naming standards

- Use snake-case for service/app names where applicable.
- Use kebab-case IDs in frontmatter (for example `my-skill-id`).
- Keep file names clear and domain-specific.

## Required metadata quality

Every artifact must include complete frontmatter with:

- identity (`id`, `name`, `version`, `owner`, `status`, `tags`)
- behavior contract (`purpose`, `input_contract`, `output_contract`, `constraints`)
- risk controls (`security`, `error_handling`)

## Local validation before PR

Run all checks before opening or updating a pull request:

```bash
python scripts/lint-frontmatter.py
python scripts/validate-index.py
python scripts/check-links.py
```

If pre-commit is installed, enable hooks:

```bash
pre-commit install
```

## Pull request rules

- Keep PRs small and easy to review (target: about 500 changed lines or less).
- Keep changes atomic and focused on one concern.
- Include what was changed and how it was validated.
- Do not add summary-only review documents unless explicitly requested.
