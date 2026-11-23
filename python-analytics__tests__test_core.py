import unittest
import pandas as pd
from benchart_ai.cleaning import clean_benchmark_frame
from benchart_ai.statistics import summarize, compare_groups

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.frame = clean_benchmark_frame(pd.DataFrame([
            {"name":"startup", "value":"100", "group":"before", "unit":"ms"},
            {"name":"startup", "value":"80", "group":"after", "unit":"ms"},
            {"name":"startup", "value":"bad", "group":"after", "unit":"ms"},
        ]))

    def test_cleaning_removes_invalid_measurements(self):
        self.assertEqual(len(self.frame), 2)

    def test_summary(self):
        result = summarize(self.frame)
        self.assertEqual(result["rows"], 2)
        self.assertEqual(len(result["benchmarks"]), 2)

    def test_compare(self):
        result = compare_groups(self.frame, "before", "after")[0]
        self.assertEqual(result["status"], "better")
        self.assertEqual(result["change_percent"], -20.0)

if __name__ == "__main__":
    unittest.main()
