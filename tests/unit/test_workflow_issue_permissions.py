"""Contract tests for the daily sync failure notification permissions."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/daily-data-sync.yml"


def workflow_permissions(workflow: str) -> dict[str, str]:
    match = re.search(
        r"(?m)^permissions:\n((?:  [a-z_]+: (?:read|write|none)\n)+)",
        workflow,
    )
    if match is None:
        raise AssertionError("workflow-level permissions block was not found")
    return {
        key: value
        for key, value in (line.strip().split(": ", maxsplit=1) for line in match[1].splitlines())
    }


def failure_alert_step(workflow: str) -> str:
    lines = workflow.splitlines()
    start = lines.index("      - name: Create issue on failure")
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].startswith("      - name: ")
        ),
        len(lines),
    )
    return "\n".join(lines[start:end])


class DailySyncIssuePermissionTests(unittest.TestCase):
    def test_failure_alert_has_issue_write_and_keeps_content_write(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertEqual(
            workflow_permissions(workflow),
            {"contents": "write", "issues": "write"},
        )
        step = failure_alert_step(workflow)
        self.assertIn("if: failure()", step)
        self.assertIn("github.rest.issues.create({", step)


if __name__ == "__main__":
    unittest.main()
