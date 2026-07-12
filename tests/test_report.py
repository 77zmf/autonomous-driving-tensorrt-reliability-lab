import json
import unittest

try:
    from . import _bootstrap
except ImportError:
    import _bootstrap

from trt_lab.report import build_report, render_json, render_markdown
from trt_lab.samples import Sample


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.report = build_report(
            [
                Sample(0, "preprocess", 1.0),
                Sample(0, "inference", 4.0),
                Sample(1, "preprocess", 3.0),
                Sample(1, "inference", 6.0),
            ]
        )

    def test_groups_component_statistics_without_mixing_scopes(self):
        self.assertNotIn("overall", self.report)
        self.assertEqual(list(self.report["components"]), ["inference", "preprocess"])
        self.assertEqual(self.report["components"]["inference"]["mean"], 5.0)
        self.assertEqual(self.report["components"]["preprocess"]["median"], 2.0)

    def test_json_output_is_valid_and_terminated(self):
        rendered = render_json(self.report)

        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(json.loads(rendered)["schema_version"], 1)

    def test_markdown_output_contains_all_metrics_and_components(self):
        rendered = render_markdown(self.report)

        self.assertIn("| Component | COUNT | MIN | MAX | MEAN | MEDIAN | P50 | P90 | P95 | P99 |", rendered)
        self.assertNotIn("Overall", rendered)
        self.assertIn("| inference | 2 | 4 | 6 | 5 |", rendered)
        self.assertIn("| preprocess | 2 | 1 | 3 | 2 |", rendered)

    def test_rejects_empty_samples(self):
        with self.assertRaisesRegex(ValueError, "without samples"):
            build_report([])


if __name__ == "__main__":
    unittest.main()
