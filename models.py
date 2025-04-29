class Expense:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def to_list(self):
        return [self.date, self.category, f"₹{float(self.amount):.2f}", self.description]

    @classmethod
    def from_list(cls, data):
        amount = float(data[2].replace('₹', '').replace(',', ''))
        return cls(data[0], data[1], amount, data[3])