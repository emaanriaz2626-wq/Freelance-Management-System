class Project:
    def __init__(self, title, deadline, rate):
        self._title = title
        self._deadline = deadline
        self._rate = rate
        self.status = "Not Started"
        self.expenses = 0.0

    def get_title(self): return self._title
    def set_title(self, title): self._title = title
    def get_deadline(self): return self._deadline
    def set_deadline(self, deadline): self._deadline = deadline
    def get_rate(self): return self._rate
    def set_rate(self, rate): self._rate = rate

    def display_info(self):
        return (f"Project: {self._title} | Deadline: {self._deadline} | Rate: ${self._rate} | "
                f"Status: {self.status} | Expenses: ${self.expenses}")

    def calculate_gross_earnings(self):
        return self._rate

    def calculate_estimated_tax(self, tax_rate=0.20):
        return self.calculate_gross_earnings() * tax_rate

    def calculate_net_income(self, tax_rate=0.20):
        return self.calculate_gross_earnings() - self.calculate_estimated_tax(tax_rate) - self.expenses

    def calculate_profit_margin(self, tax_rate=0.20):       # profit margin is the ratio of the net income to the gross earnings in percentage form.
        gross = self.calculate_gross_earnings()
        if gross == 0: return 0.0   # condition to prevent a zero division error.
        return (self.calculate_net_income(tax_rate) / gross) * 100

    def to_dict(self):
        return {
            "title": self._title,
            "deadline": self._deadline,
            "rate": self._rate,
            "status": self.status,
            "expenses": self.expenses
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data["title"], data["deadline"], data["rate"])
        p.status=data.get("status", "Not Started")
        p.expenses=data.get("expenses", 0.0)
        return p