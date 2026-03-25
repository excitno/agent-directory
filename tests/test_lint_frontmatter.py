import importlib.util
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()