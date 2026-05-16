import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List

DATA_FILE = Path("transactions.json")


@dataclass
class Transaction:
    amount: float
    category: str
    description: str
    type: str
    date: str

    def __post_init__(self):
        if self.type not in {"income", "expense"}:
            raise ValueError("type must be income or expense")
        if self.amount <= 0:
            raise ValueError("amount must be greater than zero")


class FinanceTracker:
    def __init__(self, file_path: Path = DATA_FILE):
        self.file_path = file_path
        self.transactions: List[Transaction] = []
        self.load()

    def load(self):
        if not self.file_path.exists():
            self.transactions = []
            return
        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        self.transactions = [Transaction(**item) for item in data]

    def save(self):
        data = [asdict(transaction) for transaction in self.transactions]
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_transaction(self, amount: float, category: str, description: str, type_: str):
        transaction = Transaction(
            amount=amount,
            category=category.strip().title(),
            description=description.strip(),
            type=type_.lower(),
            date=datetime.now().strftime("%Y-%m-%d")
        )
        self.transactions.append(transaction)
        self.save()

    def balance(self):
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expenses = sum(t.amount for t in self.transactions if t.type == "expense")
        return income - expenses

    def category_report(self):
        report = {}
        for transaction in self.transactions:
            if transaction.type == "expense":
                report[transaction.category] = report.get(transaction.category, 0) + transaction.amount
        return dict(sorted(report.items(), key=lambda item: item[1], reverse=True))

    def list_transactions(self):
        return self.transactions


def menu():
    tracker = FinanceTracker()

    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add income")
        print("2. Add expense")
        print("3. Show balance")
        print("4. Show category report")
        print("5. List transactions")
        print("6. Exit")

        choice = input("Choose: ").strip()

        if choice in {"1", "2"}:
            try:
                amount = float(input("Amount: "))
                category = input("Category: ")
                description = input("Description: ")
                type_ = "income" if choice == "1" else "expense"
                tracker.add_transaction(amount, category, description, type_)
                print("Transaction saved.")
            except ValueError as error:
                print("Error:", error)

        elif choice == "3":
            print(f"Current balance: ${tracker.balance():.2f}")

        elif choice == "4":
            report = tracker.category_report()
            if not report:
                print("No expense data yet.")
            for category, total in report.items():
                print(f"{category}: ${total:.2f}")

        elif choice == "5":
            if not tracker.transactions:
                print("No transactions yet.")
            for transaction in tracker.list_transactions():
                print(f"{transaction.date} | {transaction.type.upper()} | {transaction.category} | ${transaction.amount:.2f} | {transaction.description}")

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
