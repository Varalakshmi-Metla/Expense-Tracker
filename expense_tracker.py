
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt  # Optional: For graphical summaries

FILENAME = "expenses.json"  # File to store expenses

# Load expenses from file
def load_expenses():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)

# Add a new expense
def add_expense(expenses):
    try:
        amount = float(input("Enter amount: ₹"))
        category = input("Enter category (e.g., Food, Transport, etc.): ")
        date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        expense = {"amount": amount, "category": category, "date": date}
        expenses.append(expense)
        save_expenses(expenses)
        print("✅ Expense added successfully.")
    except ValueError:
        print("❌ Invalid amount entered.")

# View summaries
def view_summary(expenses):
    if not expenses:
        print("⚠️ No expenses found.")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal Spending: ₹{total:.2f}")

    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

    print("\nSpending by Category:")
    for category, amount in category_totals.items():
        print(f" - {category}: ₹{amount:.2f}")

    daily_totals = {}
    for e in expenses:
        daily_totals[e["date"]] = daily_totals.get(e["date"], 0) + e["amount"]

    print("\nSpending by Date:")
    for date, amount in sorted(daily_totals.items()):
        print(f" - {date}: ₹{amount:.2f}")

# Optional: Graphical summary
def show_graph(expenses):
    if not expenses:
        print("⚠️ No data to display.")
        return

    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Breakdown by Category")
    plt.axis("equal")
    plt.show()

# Optional: Edit or delete an expense
def edit_or_delete_expense(expenses):
    if not expenses:
        print("⚠️ No expenses to modify.")
        return

    for i, e in enumerate(expenses, 1):
        print(f"{i}. ₹{e['amount']} - {e['category']} on {e['date']}")

    try:
        idx = int(input("Select record number to edit/delete (0 to cancel): "))
        if idx == 0:
            return
        if not (1 <= idx <= len(expenses)):
            print("❌ Invalid record number.")
            return

        action = input("Type 'edit' to edit or 'delete' to delete: ").lower()

        if action == 'delete':
            del expenses[idx - 1]
            print("🗑️ Expense deleted.")
        elif action == 'edit':
            amount = float(input("Enter new amount: ₹"))
            category = input("Enter new category: ")
            date = input("Enter new date (YYYY-MM-DD): ")
            expenses[idx - 1] = {"amount": amount, "category": category, "date": date}
            print("✏️ Expense updated.")
        else:
            print("❌ Unknown action.")

        save_expenses(expenses)
    except ValueError:
        print("❌ Invalid input.")

# Main menu
def main():
    expenses = load_expenses()

    while True:
        print("\n====== Personal Expense Tracker ======")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Edit/Delete Expense")
        print("4. Show Expense Graph (optional)")
        print("5. Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            edit_or_delete_expense(expenses)
        elif choice == "4":
            show_graph(expenses)
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
