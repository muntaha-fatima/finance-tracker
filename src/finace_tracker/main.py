import questionary
from rich.console import Console
from rich.panel import Panel
from finace_tracker.features.transactions.transactions import transactions_menu
from finace_tracker.features.budgets.budgets import budgets_menu
from finace_tracker.features.analytics.analytics import analytics_menu

# Initialize Rich Console
console = Console()

def main():
    """
    Main function to display the menu and handle user choices.
    """
    console.print(Panel("[bold green]Welcome to the Personal Finance Tracker![/bold green]"))

    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Manage Transactions",
                "Manage Budgets",
                "View Analytics",
                "Exit",
            ],
        ).ask()

        if choice == "Manage Transactions":
            transactions_menu()
        elif choice == "Manage Budgets":
            budgets_menu()
        elif choice == "View Analytics":
            analytics_menu()
        elif choice == "Exit" or choice is None:
            console.print("[bold green]Goodbye![/bold green]")
            break


if __name__ == "__main__":
    main()
