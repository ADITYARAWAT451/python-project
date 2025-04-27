import csv
from pathlib import Path
from models import Expense

FILENAME = "expenses.csv"

def ensure_file_exists():
    """Create the file with headers if it doesn't exist"""
    if not Path(FILENAME).exists():
        with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

def add_expense_to_file(expense: Expense):
    """Append a new expense to the CSV file"""
    ensure_file_exists()
    with open(FILENAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([expense.date, expense.category, expense.amount, expense.description])

def read_expenses_from_file():
    """Read all expenses from the CSV file"""
    ensure_file_exists()
    expenses = []
    with open(FILENAME, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if row:
                expenses.append(Expense.from_list(row))
    return expenses

def clear_all_expenses():
    """Clear all expenses (keeping headers)"""
    ensure_file_exists()
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])