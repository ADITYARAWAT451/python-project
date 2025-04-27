from dataclasses import dataclass

@dataclass
class Expense:
    date: str
    category: str
    amount: float
    description: str

    def to_list(self):
        return [self.date, self.category, f"₹{float(self.amount):.2f}", self.description]

    @staticmethod
    def from_list(data):
        amount = float(data[2].replace('₹', '').replace(',', ''))
        return Expense(data[0], data[1], amount, data[3])