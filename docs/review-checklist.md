# Review checklist

Use this checklist for systematic pull request reviews on this repository.

## Artifact completeness

- [ ] Each new or changed artifact uses the correct template structure.
- [ ] Required frontmatter fields are present and meaningful.
- [ ] ID and version format are valid.
- [ ] Status value is valid (`draft`, `active`, `deprecated`).

## Index integrity

- [ ] `index.yaml` entries exist for new artifacts.
- [ ] Index paths reference existing files in the correct domain folder.
- [ ] No duplicate IDs within an index.
- [ ] IDs are unique across repository artifacts.

## Security and error handling

- [ ] Security boundaries are documented in artifact metadata/content.
- [ ] Error handling behavior is documented and actionable.
- [ ] No sensitive data, keys, or credentials are introduced.

## Repository quality gates

- [ ] Frontmatter lint passes.
- [ ] Index validation passes.
- [ ] Internal link checks pass.
- [ ] CI workflow is green for the PR.

## Reviewability

- [ ] Change scope is focused and easy to verify.
- [ ] PR size remains reviewable (target: about 500 changed lines or less).
- [ ] Validation steps are included in PR description.
