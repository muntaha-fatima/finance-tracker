from rich.console import Console
from rich.table import Table
from collections import defaultdict
import datetime
import questionary
from finace_tracker.database import load_transactions, load_budgets

console = Console()

def spending_analysis():
    """
    Analyzes spending patterns and displays insights.
    """
    transactions = load_transactions()
    if not transactions:
        console.print("[bold yellow]No transactions available for analysis.[/bold yellow]")
        return

    # Filter for expenses in the current month
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    monthly_expenses = [
        t for t in transactions
        if t["type"] == "Expense" and
           datetime.date.fromisoformat(t["date"]).month == current_month and
           datetime.date.fromisoformat(t["date"]).year == current_year
    ]

    if not monthly_expenses:
        console.print("[bold yellow]No expenses recorded for the current month.[/bold yellow]")
        return

    # 1. Breakdown by category
    category_spending = defaultdict(int)
    total_spending = 0
    for t in monthly_expenses:
        category_spending[t["category"]] += t["amount"]
        total_spending += t["amount"]

    table = Table(title=f"Spending Breakdown for {datetime.date.today().strftime('%B %Y')}")
    table.add_column("Category", style="green")
    table.add_column("Amount", justify="right", style="yellow")
    table.add_column("% of Total", justify="right", style="cyan")

    for category, amount in sorted(category_spending.items(), key=lambda item: item[1], reverse=True):
        percentage = (amount / total_spending) * 100 if total_spending else 0
        table.add_row(category, f"{amount / 100:.2f}", f"{percentage:.2f}%")

    console.print(table)

    # 2. Top 3 spending categories
    top_3 = sorted(category_spending.items(), key=lambda item: item[1], reverse=True)[:3]
    console.print("\n[bold]Top 3 Spending Categories:[/bold]")
    for i, (category, amount) in enumerate(top_3):
        console.print(f"{i+1}. {category}: {amount / 100:.2f}")

    # 3. Average daily expense
    num_days_in_month = (datetime.date.today().day)
    avg_daily_expense = total_spending / num_days_in_month if num_days_in_month else 0
    console.print(f"\n[bold]Average Daily Expense:[/bold] {avg_daily_expense / 100:.2f}")


def income_analysis():
    """
    Analyzes income patterns and displays insights.
    """
    transactions = load_transactions()
    if not transactions:
        console.print("[bold yellow]No transactions available for analysis.[/bold yellow]")
        return

    # Filter for income in the current month
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    monthly_income = [
        t for t in transactions
        if t["type"] == "Income" and
           datetime.date.fromisoformat(t["date"]).month == current_month and
           datetime.date.fromisoformat(t["date"]).year == current_year
    ]

    if not monthly_income:
        console.print("[bold yellow]No income recorded for the current month.[/bold yellow]")
        return

    # 1. Income by source
    source_income = defaultdict(int)
    total_income = 0
    for t in monthly_income:
        source_income[t["category"]] += t["amount"]
        total_income += t["amount"]

    table = Table(title=f"Income Breakdown for {datetime.date.today().strftime('%B %Y')}")
    table.add_column("Source", style="green")
    table.add_column("Amount", justify="right", style="yellow")

    for source, amount in sorted(source_income.items(), key=lambda item: item[1], reverse=True):
        table.add_row(source, f"{amount / 100:.2f}")

    console.print(table)

    # 2. Total income this month
    console.print(f"\n[bold]Total Income This Month:[/bold] {total_income / 100:.2f}")


def savings_analysis():
    """
    Analyzes savings and displays insights.
    """
    transactions = load_transactions()
    if not transactions:
        console.print("[bold yellow]No transactions available for analysis.[/bold yellow]")
        return

    # Filter for income and expenses in the current month
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year

    monthly_income = sum(
        t["amount"] for t in transactions
        if t["type"] == "Income" and
           datetime.date.fromisoformat(t["date"]).month == current_month and
           datetime.date.fromisoformat(t["date"]).year == current_year
    )
    monthly_expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "Expense" and
           datetime.date.fromisoformat(t["date"]).month == current_month and
           datetime.date.fromisoformat(t["date"]).year == current_year
    )

    monthly_savings = monthly_income - monthly_expenses
    savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

    console.print(f"\n[bold]Savings for {datetime.date.today().strftime('%B %Y')}:[/bold]")
    console.print(f"  [green]Total Income:[/green] {monthly_income / 100:.2f}")
    console.print(f"  [red]Total Expenses:[/red] {monthly_expenses / 100:.2f}")
    console.print(f"  [bold blue]Net Savings:[/bold blue] {monthly_savings / 100:.2f}")
    console.print(f"  [bold cyan]Savings Rate:[/bold cyan] {savings_rate:.2f}%")


def financial_health_score():
    """
    Calculates and displays a financial health score.
    """
    transactions = load_transactions()
    budgets = load_budgets()

    if not transactions:
        console.print("[bold yellow]No transactions available for analysis.[/bold yellow]")
        return

    # --- Calculations ---
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year

    monthly_income = sum(
        t["amount"] for t in transactions
        if t["type"] == "Income" and
           datetime.date.fromisoformat(t["date"]).month == current_month and
           datetime.date.fromisoformat(t["date"]).year == current_year
    )
    monthly_expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "Expense" and
           datetime.date.fromisoformat(t["date"]).month == current_month and
           datetime.date.fromisoformat(t["date"]).year == current_year
    )
    monthly_savings = monthly_income - monthly_expenses
    savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

    # --- Scoring ---
    score = 0
    # 1. Savings Rate (40 points)
    if savings_rate >= 20:
        score += 40
    elif savings_rate >= 10:
        score += 20
    elif savings_rate > 0:
        score += 10

    # 2. Budget Adherence (30 points)
    if budgets:
        total_budgeted = sum(budgets.values())
        if total_budgeted > 0:
            if monthly_expenses <= total_budgeted:
                score += 30
            elif monthly_expenses <= total_budgeted * 1.1: # Within 10% over
                score += 15

    # 3. Income vs Expenses (30 points)
    if monthly_income > monthly_expenses:
        score += 30
    elif monthly_income > monthly_expenses * 0.9: # Expenses are not more than 10% of income
        score += 15

    # --- Display ---
    console.print(f"\n[bold]Financial Health Score: {score}/100[/bold]")
    if score >= 80:
        console.print("[bold green]Excellent! You are doing a great job managing your finances.[/bold green]")
    elif score >= 50:
        console.print("[bold yellow]Good. There are some areas for improvement.[/bold yellow]")
    else:
        console.print("[bold red]Needs Improvement. Let's work on getting this score up.[/bold red]")


def analytics_menu():
    """
    Displays the menu for financial analytics.
    """
    while True:
        choice = questionary.select(
            "Financial Analytics",
            choices=["Spending Analysis", "Income Analysis", "Savings Analysis", "Financial Health Score", "Back to Main Menu"],
        ).ask()

        if choice == "Spending Analysis":
            spending_analysis()
        elif choice == "Income Analysis":
            income_analysis()
        elif choice == "Savings Analysis":
            savings_analysis()
        elif choice == "Financial Health Score":
            financial_health_score()
        elif choice == "Back to Main Menu" or choice is None:
            break
