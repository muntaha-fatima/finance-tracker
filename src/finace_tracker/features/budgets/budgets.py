import questionary
from rich.console import Console
from rich.table import Table
from finace_tracker.database import load_budgets, save_budgets

# Initialize Rich Console
console = Console()

# In-memory data store for budgets
budgets = {}

# Categories from gemini.md
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]


def set_budget():
    """Sets a budget for a specific category."""
    category = questionary.select(
        "Select a category to set a budget for:",
        choices=EXPENSE_CATEGORIES,
    ).ask()

    if category is None:
        return

    amount_str = questionary.text(f"Enter the budget amount for {category}:").ask()
    if amount_str is None:
        return

    try:
        # Store amount in cents
        amount = int(float(amount_str) * 100)
    except ValueError:
        console.print("[bold red]Invalid amount. Please enter a number.[/bold red]")
        return

    budgets[category] = amount
    save_budgets(budgets)
    console.print(f"[bold green]Budget for {category} set to {amount / 100:.2f}[/bold green]")


def view_budgets():
    """Displays all set budgets in a table."""
    if not budgets:
        console.print("[bold yellow]No budgets set.[/bold yellow]")
        return

    table = Table(title="Monthly Budgets")
    table.add_column("Category", style="green")
    table.add_column("Budget", justify="right", style="yellow")

    for category, amount in budgets.items():
        display_amount = f"{amount / 100:.2f}"
        table.add_row(category, display_amount)

    console.print(table)


def budgets_menu():
    """
    Displays the menu for budget management.
    """
    global budgets
    budgets = load_budgets()
    while True:
        choice = questionary.select(
            "Budget Management",
            choices=["Set Budget", "View Budgets", "Back to Main Menu"],
        ).ask()

        if choice == "Set Budget":
            set_budget()
        elif choice == "View Budgets":
            view_budgets()
        elif choice == "Back to Main Menu" or choice is None:
            break
