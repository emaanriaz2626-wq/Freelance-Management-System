class Client:
    def __init__(self, name, contact, payment_terms, currency="USD"):
        self._name = name
        self._contact = contact
        self._payment_terms = payment_terms
        self.currency = currency

    def get_name(self): return self._name
    def set_name(self, name): self._name = name
    def get_contact(self): return self._contact
    def set_contact(self, contact): self._contact = contact
    def get_payment_terms(self): return self._payment_terms
    def set_payment_terms(self, terms): self._payment_terms = terms

    def display_info(self):
        return f"Client Name: {self._name} | Contact: {self._contact} | Payment Terms: {self._payment_terms} | Currency: {self.currency}"

    def to_dict(self):
        #convert to dict
        return {
            "name": self._name,
            "contact": self._contact,
            "payment_terms": self._payment_terms,
            "currency": self.currency
        }

    @classmethod
    def from_dict(cls, data):
        #create from dict
        return cls(data["name"], data["contact"], data["payment_terms"], data.get("currency", "USD"))
