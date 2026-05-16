import tempfile
import unittest
from pathlib import Path

from app import FinanceTracker


class TestFinanceTracker(unittest.TestCase):
    def test_balance_and_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tracker = FinanceTracker(Path(temp_dir) / "test_transactions.json")
            tracker.add_transaction(1000, "salary", "monthly salary", "income")
            tracker.add_transaction(250, "food", "groceries", "expense")
            tracker.add_transaction(100, "food", "restaurant", "expense")

            self.assertEqual(tracker.balance(), 650)
            self.assertEqual(tracker.category_report()["Food"], 350)


if __name__ == "__main__":
    unittest.main()
