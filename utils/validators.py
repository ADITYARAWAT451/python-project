from datetime import datetime

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_amount(amount_str):
    """Validate amount is a positive number"""
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False