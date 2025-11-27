import questionary
from rich.console import Console
from rich.table import Table
import datetime
from finace_tracker.database import load_transactions, save_transactions

# Initialize Rich Console
console = Console()

# In-memory data store for transactions
transactions = []

# Transaction categories from gemini.md
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]


def add_transaction():
    """Adds a new transaction (expense or income)."""
    transaction_type = questionary.select(
        "Select transaction type:",
        choices=["Expense", "Income"],
    ).ask()

    if transaction_type is None:
        return

    if transaction_type == "Expense":
        category = questionary.select("Select expense category:", choices=EXPENSE_CATEGORIES).ask()
    else:
        category = questionary.select("Select income category:", choices=INCOME_CATEGORIES).ask()

    if category is None:
        return

    amount_str = questionary.text("Enter the amount:").ask()
    if amount_str is None:
        return

    try:
        # Store amount in cents
        amount = int(float(amount_str) * 100)
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    description = questionary.text("Enter a description:").ask()
    if description is None:
        return

    transaction = {
        "date": datetime.date.today().isoformat(),
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description,
    }

    transactions.append(transaction)
    save_transactions(transactions)
    console.print("[bold green]Transaction added successfully![/bold green]")


def view_transactions():
    """Displays all transactions in a table."""
    if not transactions:
        console.print("[bold yellow]No transactions to display.[/bold yellow]")
        return

    table = Table(title="All Transactions")
    table.add_column("Date", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Amount", justify="right", style="yellow")
    table.add_column("Description", style="white")

    for t in transactions:
        # Display amount in currency format
        display_amount = f"{t['amount'] / 100:.2f}"
        table.add_row(
            t["date"],
            t["type"],
            t["category"],
            display_amount,
            t["description"],
        )

    console.print(table)


def transactions_menu():
    """
    Displays the menu for transaction management.
    """
    global transactions
    transactions = load_transactions()
    while True:
        choice = questionary.select(
            "Transaction Management",
            choices=["Add Transaction", "View Transactions", "Back to Main Menu"],
        ).ask()

        if choice == "Add Transaction":
            add_transaction()
        elif choice == "View Transactions":
            view_transactions()
        elif choice == "Back to Main Menu" or choice is None:
            break
