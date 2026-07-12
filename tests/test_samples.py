import io
import tempfile
import unittest
from pathlib import Path

try:
    from . import _bootstrap
except ImportError:
    import _bootstrap

from trt_lab.samples import (
    Sample,
    SampleValidationError,
    load_samples,
    parse_csv,
    parse_jsonl,
)


class JsonlParsingTests(unittest.TestCase):
    def test_parses_samples_and_ignores_blank_lines(self):
        stream = io.StringIO(
            '{"iteration": 0, "component": " inference ", "latency_ms": 1}\n'
            "\n"
            '{"iteration": 1, "component": "inference", "latency_ms": 2.5, "tag": "warm"}\n'
        )

        self.assertEqual(
            parse_jsonl(stream),
            [Sample(0, "inference", 1.0), Sample(1, "inference", 2.5)],
        )

    def test_rejects_malformed_json(self):
        with self.assertRaisesRegex(SampleValidationError, "JSONL line 1: invalid JSON"):
            parse_jsonl(io.StringIO("{bad}\n"))

    def test_rejects_non_object(self):
        with self.assertRaisesRegex(SampleValidationError, "must be a JSON object"):
            parse_jsonl(io.StringIO("[]\n"))


class CsvParsingTests(unittest.TestCase):
    def test_parses_csv_with_extra_columns(self):
        stream = io.StringIO(
            "iteration,component,latency_ms,note\n"
            "0,preprocess,0.25,baseline\n"
            "1,inference,3.5,baseline\n"
        )

        self.assertEqual(
            parse_csv(stream),
            [Sample(0, "preprocess", 0.25), Sample(1, "inference", 3.5)],
        )

    def test_rejects_missing_header_field(self):
        with self.assertRaisesRegex(SampleValidationError, "missing required field"):
            parse_csv(io.StringIO("iteration,component\n0,inference\n"))

    def test_rejects_extra_values(self):
        with self.assertRaisesRegex(SampleValidationError, "more values than the header"):
            parse_csv(
                io.StringIO("iteration,component,latency_ms\n0,inference,1.0,extra\n")
            )


class SchemaValidationTests(unittest.TestCase):
    def assert_invalid_json_sample(self, record: str, message: str):
        with self.assertRaisesRegex(SampleValidationError, message):
            parse_jsonl(io.StringIO(record + "\n"))

    def test_rejects_missing_field(self):
        self.assert_invalid_json_sample(
            '{"iteration": 0, "component": "inference"}', "missing required field"
        )

    def test_rejects_negative_iteration(self):
        self.assert_invalid_json_sample(
            '{"iteration": -1, "component": "inference", "latency_ms": 1}',
            "iteration must be a non-negative integer",
        )

    def test_rejects_boolean_iteration(self):
        self.assert_invalid_json_sample(
            '{"iteration": true, "component": "inference", "latency_ms": 1}',
            "iteration must be a non-negative integer",
        )

    def test_rejects_empty_component(self):
        self.assert_invalid_json_sample(
            '{"iteration": 0, "component": " ", "latency_ms": 1}',
            "component must be a non-empty string",
        )

    def test_rejects_negative_non_finite_and_boolean_latency(self):
        for latency in ("-1", "NaN", "Infinity", "true"):
            with self.subTest(latency=latency):
                self.assert_invalid_json_sample(
                    f'{{"iteration": 0, "component": "inference", "latency_ms": {latency}}}',
                    "latency_ms must be a non-negative finite number",
                )

    def test_rejects_empty_input(self):
        with self.assertRaisesRegex(SampleValidationError, "no samples"):
            parse_jsonl(io.StringIO("\n"))

    def test_load_samples_infers_format(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "samples.csv"
            path.write_text(
                "iteration,component,latency_ms\n0,inference,1.25\n",
                encoding="utf-8",
            )
            self.assertEqual(load_samples(path), [Sample(0, "inference", 1.25)])


if __name__ == "__main__":
    unittest.main()
