import unittest

try:
    from . import _bootstrap
except ImportError:
    import _bootstrap

from trt_lab.statistics import percentile, summarize_values


class PercentileTests(unittest.TestCase):
    def test_uses_linear_interpolation(self):
        values = [0, 10, 20, 30, 40]

        self.assertEqual(percentile(values, 0.50), 20.0)
        self.assertEqual(percentile(values, 0.90), 36.0)
        self.assertEqual(percentile(values, 0.95), 38.0)
        self.assertAlmostEqual(percentile(values, 0.99), 39.6)

    def test_interpolates_two_values(self):
        self.assertEqual(percentile([1, 2], 0.5), 1.5)

    def test_rejects_invalid_probability(self):
        with self.assertRaisesRegex(ValueError, "between 0 and 1"):
            percentile([1], 1.1)


class SummaryTests(unittest.TestCase):
    def test_computes_all_metrics(self):
        summary = summarize_values([4, 1, 3, 2])

        self.assertEqual(summary["count"], 4)
        self.assertEqual(summary["min"], 1.0)
        self.assertEqual(summary["max"], 4.0)
        self.assertEqual(summary["mean"], 2.5)
        self.assertEqual(summary["median"], 2.5)
        self.assertEqual(summary["p50"], 2.5)
        self.assertAlmostEqual(summary["p90"], 3.7)
        self.assertAlmostEqual(summary["p95"], 3.85)
        self.assertAlmostEqual(summary["p99"], 3.97)

    def test_rejects_empty_negative_and_non_finite_values(self):
        for values in ([], [-1], [float("nan")], [float("inf")], [True]):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    summarize_values(values)


if __name__ == "__main__":
    unittest.main()
