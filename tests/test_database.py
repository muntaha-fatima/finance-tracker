import unittest
import os
import csv
from finace_tracker.database import (
    load_transactions,
    save_transactions,
    load_budgets,
    save_budgets,
)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up test files."""
        self.transactions_file = "test_transactions.txt"
        self.budgets_file = "test_budgets.txt"
        # Override the file paths in the database module
        import finace_tracker.database
        finace_tracker.database.TRANSACTIONS_FILE = self.transactions_file
        finace_tracker.database.BUDGETS_FILE = self.budgets_file

    def tearDown(self):
        """Tear down test files."""
        if os.path.exists(self.transactions_file):
            os.remove(self.transactions_file)
        if os.path.exists(self.budgets_file):
            os.remove(self.budgets_file)

    def test_save_and_load_transactions(self):
        """Test saving and loading transactions."""
        transactions = [
            {"date": "2025-01-01", "type": "Expense", "category": "Food", "amount": 1000, "description": "Lunch"},
            {"date": "2025-01-02", "type": "Income", "category": "Salary", "amount": 50000, "description": "Paycheck"},
        ]
        save_transactions(transactions)
        loaded_transactions = load_transactions()
        self.assertEqual(loaded_transactions, transactions)

    def test_load_transactions_corrupted(self):
        """Test loading transactions from a corrupted file."""
        with open(self.transactions_file, "w", newline="") as f:
            f.write("date,type,category,amount,description\n")
            f.write("2025-01-01,Expense,Food,10.00,Lunch\n") # Amount is float
            f.write("2025-01-02,Income,Salary,invalid,Paycheck\n") # Amount is not a number

        loaded_transactions = load_transactions()
        self.assertEqual(len(loaded_transactions), 0)

    def test_save_and_load_budgets(self):
        """Test saving and loading budgets."""
        budgets = {"Food": 50000, "Transport": 20000}
        save_budgets(budgets)
        loaded_budgets = load_budgets()
        self.assertEqual(loaded_budgets, budgets)

    def test_load_budgets_corrupted(self):
        """Test loading budgets from a corrupted file."""
        with open(self.budgets_file, "w", newline="") as f:
            f.write("Food,500.00\n") # Amount is float
            f.write("Transport,invalid\n") # Amount is not a number

        loaded_budgets = load_budgets()
        # The current implementation will skip the corrupted rows.
        # So the loaded_budgets will be empty.
        self.assertEqual(len(loaded_budgets), 0)

if __name__ == "__main__":
    unittest.main()
