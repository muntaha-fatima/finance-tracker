import csv
from rich.console import Console

console = Console()

TRANSACTIONS_FILE = "database/transactions.txt"
BUDGETS_FILE = "database/budgets.txt"


def load_transactions():
    """Loads transactions from the CSV file."""
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["amount"] = int(row["amount"])
                    transactions.append(row)
                except (ValueError, KeyError) as e:
                    console.print(f"[bold yellow]Warning: Skipping corrupted transaction row: {row}. Error: {e}[/bold yellow]")
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet
    except csv.Error as e:
        console.print(f"[bold red]Error reading transactions file: {e}[/bold red]")
    return transactions


def save_transactions(transactions):
    """Saves all transactions to the CSV file."""
    try:
        with open(TRANSACTIONS_FILE, "w", newline="") as file:
            if not transactions:
                return
            writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
            writer.writeheader()
            writer.writerows(transactions)
    except IOError as e:
        console.print(f"[bold red]Error writing transactions file: {e}[/bold red]")


def load_budgets():
    """Loads budgets from the CSV file."""
    budgets = {}
    try:
        with open(BUDGETS_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    try:
                        budgets[row[0]] = int(row[1])
                    except (ValueError, IndexError) as e:
                        console.print(f"[bold yellow]Warning: Skipping corrupted budget row: {row}. Error: {e}[/bold yellow]")
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet
    except csv.Error as e:
        console.print(f"[bold red]Error reading budgets file: {e}[/bold red]")
    return budgets


def save_budgets(budgets):
    """Saves all budgets to the CSV file."""
    try:
        with open(BUDGETS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            for category, amount in budgets.items():
                writer.writerow([category, amount])
    except IOError as e:
        console.print(f"[bold red]Error writing budgets file: {e}[/bold red]")
