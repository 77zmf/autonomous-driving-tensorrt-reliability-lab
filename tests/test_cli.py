import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

try:
    from . import _bootstrap
except ImportError:
    import _bootstrap

from trt_lab.cli import main


class CliTests(unittest.TestCase):
    def test_writes_json_to_stdout(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "samples.jsonl"
            input_path.write_text(
                '{"iteration": 0, "component": "inference", "latency_ms": 2}\n',
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main([str(input_path)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(stdout.getvalue())["components"]["inference"]["p99"], 2.0
        )

    def test_reads_csv_from_stdin_and_writes_markdown_file(self):
        stdin = io.StringIO(
            "iteration,component,latency_ms\n0,preprocess,0.5\n"
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "report.md"
            with mock.patch("sys.stdin", stdin):
                exit_code = main(
                    [
                        "-",
                        "--input-format",
                        "csv",
                        "--format",
                        "markdown",
                        "--output",
                        str(output_path),
                    ]
                )
            rendered = output_path.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn("| preprocess | 1 | 0.5 |", rendered)

    def test_reports_validation_error(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "bad.jsonl"
            input_path.write_text(
                '{"iteration": 0, "component": "inference", "latency_ms": -1}\n',
                encoding="utf-8",
            )
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                exit_code = main([str(input_path)])

        self.assertEqual(exit_code, 2)
        self.assertIn("non-negative finite number", stderr.getvalue())

    def test_requires_input_format_for_stdin(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(["-"])

        self.assertEqual(exit_code, 2)
        self.assertIn("--input-format is required", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
