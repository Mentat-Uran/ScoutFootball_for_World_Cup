"""Contract tests for manually selected ingestion sources."""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/daily-data-sync.yml"


def ingestion_step() -> tuple[str, str]:
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    start = lines.index("      - name: Run data ingestion")
    end = next(
        index
        for index in range(start + 1, len(lines))
        if lines[index].startswith("      - name: ")
    )
    step_lines = lines[start:end]
    run_start = step_lines.index("        run: |") + 1
    script_lines = []
    for line in step_lines[run_start:]:
        if not line.strip():
            script_lines.append("")
        elif line.startswith("          "):
            script_lines.append(line[10:])
        else:
            break
    return "\n".join(step_lines), "\n".join(script_lines)


class WorkflowSourceInputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.workdir = Path(self.temp_dir.name)
        self.bin_dir = self.workdir / "bin"
        self.bin_dir.mkdir()
        fake_uv = self.bin_dir / "uv"
        fake_uv.write_text(
            "#!/usr/bin/env bash\n"
            "printf '%s\\n' \"$@\" > \"$UV_ARGS_FILE\"\n"
            "printf 'fake ingestion completed\\n'\n",
            encoding="utf-8",
        )
        fake_uv.chmod(0o755)
        self.args_file = self.workdir / "uv-args.txt"
        self.step, self.script = ingestion_step()

    def run_step(self, sources: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            {
                "PATH": f"{self.bin_dir}{os.pathsep}{environment['PATH']}",
                "REQUESTED_SOURCES": sources,
                "UV_ARGS_FILE": str(self.args_file),
            }
        )
        return subprocess.run(
            ["bash", "-e", "-c", self.script],
            check=False,
            cwd=self.workdir,
            env=environment,
            capture_output=True,
            text=True,
        )

    def test_input_expression_is_confined_to_env_and_write_permission_remains(self) -> None:
        self.assertEqual(self.step.count("${{ inputs.sources ||"), 1)
        self.assertIn(
            "REQUESTED_SOURCES: ${{ inputs.sources || 'football_data,clubelo' }}",
            self.step,
        )
        self.assertNotIn("${{", self.script)
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(workflow, re.compile(r"(?m)^permissions:\n  contents: write$"))

    def test_comma_separated_sources_become_separate_cli_arguments(self) -> None:
        result = self.run_step("football_data, clubelo")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.args_file.read_text(encoding="utf-8").splitlines(),
            [
                "run",
                "python",
                "-m",
                "scoutfootball",
                "ingest",
                "--sources",
                "football_data",
                "clubelo",
            ],
        )

    def test_pipeline_supported_sources_are_all_accepted(self) -> None:
        sources = (
            "statsbomb_open",
            "football_data",
            "clubelo",
            "understat",
            "sofascore",
            "sofifa",
            "api_football",
            "transfermarkt_datasets",
        )
        result = self.run_step(",".join(sources))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.args_file.read_text(encoding="utf-8").splitlines()[-len(sources) :],
            list(sources),
        )

    def test_unsupported_source_is_rejected_before_uv_runs(self) -> None:
        result = self.run_step("football_data,unknown_provider")

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.args_file.exists())

    def test_shell_metacharacters_are_plain_input_and_never_execute(self) -> None:
        marker = self.workdir / "command-was-executed"
        payloads = (
            f"clubelo$(touch {marker})",
            f"clubelo; touch {marker}",
        )

        for payload in payloads:
            with self.subTest(payload=payload):
                self.args_file.unlink(missing_ok=True)
                result = self.run_step(payload)

                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(marker.exists())
                self.assertFalse(self.args_file.exists())


if __name__ == "__main__":
    unittest.main()
