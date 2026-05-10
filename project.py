class Project:
    def __init__(self, title, deadline, rate, rate_type):
        self._title = title
        self._deadline = deadline
        self.rate_type = rate_type #fixed or hourly
        self._rate = rate
        self.status = "Not Started"
        self.expenses = 0.0
        self.hours_worked = 0.0

    def get_title(self): return self._title
    def set_title(self, title): self._title = title
    def get_deadline(self): return self._deadline
    def set_deadline(self, deadline): self._deadline = deadline
    def get_rate(self): return self._rate
    def set_rate(self, rate): self._rate = rate

    def display_info(self):
        return (f"Project: {self._title} | Deadline: {self._deadline} | Rate: ${self._rate} | "
                f"Status: {self.status} | Hours Worked: {self.hours_worked} |Expenses: ${self.expenses}")

    def calculate_gross_earnings(self):
        if self.rate_type == "fixed":
            return self._rate
        elif self.rate_type == "hourly":
            return self.hours_worked * self._rate

    def calculate_estimated_tax(self, tax_rate=0.20):
        return self.calculate_gross_earnings() * tax_rate

    def calculate_net_income(self, tax_rate=0.20):
        return self.calculate_gross_earnings() - self.calculate_estimated_tax(tax_rate) - self.expenses

    def calculate_profit_margin(self, tax_rate=0.20):       #calculate margin
        gross = self.calculate_gross_earnings()
        if gross == 0: return 0.0   #prevent zero division
        return (self.calculate_net_income(tax_rate) / gross) * 100

    def to_dict(self):
        return {
            "title": self._title,
            "deadline": self._deadline,
            "rate": self._rate,
            "rate_type": self.rate_type,
            "status": self.status,
            "expenses": self.expenses,
            "hours_worked": self.hours_worked
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data["title"], data["deadline"], data["rate"], data.get("rate_type", "fixed"))
        p.status=data.get("status", "Not Started")
        p.expenses=data.get("expenses", 0.0)
        p.hours_worked=data.get("hours_worked", 0.0)
        return p