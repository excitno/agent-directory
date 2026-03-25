import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "lint-frontmatter.py"
SPEC = importlib.util.spec_from_file_location("lint_frontmatter", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load module spec for {MODULE_PATH}")
LINT_FRONTMATTER = importlib.util.module_from_spec(SPEC)
if LINT_FRONTMATTER is None:
    raise RuntimeError(f"Unable to create module from spec for {MODULE_PATH}")
SPEC.loader.exec_module(LINT_FRONTMATTER)


class ParseFrontmatterTests(unittest.TestCase):
    def test_closing_delimiter_allows_trailing_whitespace(self) -> None:
        text = "---\nid: example-id\n---  \n"

        data, errors = LINT_FRONTMATTER.parse_frontmatter(text)

        self.assertEqual(data.get("id"), "example-id")
        self.assertEqual(errors, [])

    def test_empty_required_scalar_field_is_reported_missing(self) -> None:
        content = """---
id:
name: Example Subagent
version: v0.1.0
owner: platform-team
status: draft
tags:
  - orchestration
purpose: Execute focused research and execution tasks with a predictable output contract.
input_contract: Receives a scoped objective, constraints, and optional context references.
output_contract: Returns a structured result with findings, actions taken, and unresolved risks.
constraints:
  - Do not perform destructive operations.
security: Avoid exposing secrets and do not access protected resources without explicit approval.
error_handling: Report errors with context, stop on unsafe conditions, and suggest safe next steps.
---
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example-subagent.md"
            path.write_text(content, encoding="utf-8")
            errors, _ = LINT_FRONTMATTER.validate_file(path, "subagents")

        self.assertTrue(any("missing required frontmatter field 'id'" in err for err in errors))


if __name__ == "__main__":
    unittest.main()