"""Contract tests for the daily sync failure notification permissions."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/daily-data-sync.yml"


def workflow_permissions(workflow: str) -> dict[str, str]:
    match = re.search(
        r"(?m)^permissions:\n((?:  [a-z_-]+: (?:read|write|none)\n)+)",
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
    def test_failure_alert_uses_only_existing_repository_label(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        step = failure_alert_step(workflow)

        self.assertRegex(step, r"(?m)^\s+labels: \['automation'\]$")
        self.assertNotIn("'data-sync'", step)

    def test_failure_alert_has_issue_write_and_keeps_content_write(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertEqual(
            workflow_permissions(workflow),
            {"contents": "write", "issues": "write"},
        )
        step = failure_alert_step(workflow)
        self.assertIn("if: failure()", step)
        self.assertIn("github.rest.issues.create({", step)

    def test_hyphenated_extra_permission_scope_fails_exact_scope_check(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        workflow_with_extra_scope = workflow.replace(
            "  issues: write\n",
            "  issues: write\n  id-token: write\n",
            1,
        )
        expected_permissions = {"contents": "write", "issues": "write"}
        parsed_permissions = workflow_permissions(workflow_with_extra_scope)

        self.assertEqual(
            parsed_permissions,
            {**expected_permissions, "id-token": "write"},
        )
        with self.assertRaises(AssertionError):
            self.assertEqual(parsed_permissions, expected_permissions)


if __name__ == "__main__":
    unittest.main()
