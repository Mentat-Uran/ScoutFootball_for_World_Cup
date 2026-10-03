"""Contract tests for workflow shell failure propagation."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]


class WorkflowPipefailTests(unittest.TestCase):
    def test_piped_data_workflows_use_explicit_bash(self) -> None:
        workflow_paths = (
            ROOT / ".github/workflows/daily-data-sync.yml",
            ROOT / ".github/workflows/data-validation.yml",
        )

        for path in workflow_paths:
            with self.subTest(workflow=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertRegex(
                    content,
                    re.compile(r"(?m)^defaults:\n  run:\n    shell: bash\s*$"),
                )
                self.assertRegex(content, r"\|\s*tee\b")


if __name__ == "__main__":
    unittest.main()
