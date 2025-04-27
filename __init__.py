"""
Expense Tracker Application

A modular personal finance application for tracking expenses with CSV storage.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

# Import key components to make them easily accessible
from models import Expense
from file_operations import (
    add_expense_to_file,
    read_expenses_from_file,
    clear_all_expenses
)

# Package-level initialization
def init_app():
    """Initialize application resources"""
    from .file_operations import ensure_file_exists
    ensure_file_exists()