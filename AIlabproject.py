import os  #WHY///
import json

class Client:
    def __init__(self, name, contact, payment_terms):
        self._name = name
        self._contact = contact
        self._payment_terms = payment_terms

    def get_name(self): return self._name
    def set_name(self, name): self._name = name
    def get_contact(self): return self._contact
    def set_contact(self, contact): self._contact = contact
    def get_payment_terms(self): return self._payment_terms
    def set_payment_terms(self, terms): self._payment_terms = terms

    def display_info(self):
        return f"Client Name: {self._name} | Contact: {self._contact} | Payment Terms: {self._payment_terms}"

    def to_dict(self):
        return {
            "name": self._name,
            "contact": self._contact,
            "payment_terms": self._payment_terms
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["contact"], data["payment_terms"])

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

class Invoice:
    def __init__(self, client, project, due_date):
        self._client = client
        self._project = project
        self._due_date = due_date
        self._items = []

    def add_item(self, description, amount):
        self._items.append({"description": description, "amount": amount})
        
    def clear_items(self):
        self._items = []

    def get_client(self): return self._client
    def get_project(self): return self._project
    def get_due_date(self): return self._due_date
    def set_due_date(self, due_date): self._due_date = due_date
    def get_items(self): return self._items

    def get_totals(self):
        return sum(item["amount"] for item in self._items)

    def display_info(self):
        info = f"Invoice for {self._client.get_name()} (Project: {self._project.get_title()}) - Due: {self._due_date}\n"
        for idx, item in enumerate(self._items, 1):
            info += f"  {idx}. {item['description']}: ${item['amount']:.2f}\n"
        info += f"  Total: ${self.get_totals():.2f}"
        return info

    def to_dict(self, clients_list, projects_list):
        return {
            "client_idx": clients_list.index(self._client) if self._client in clients_list else -1,
            "project_idx": projects_list.index(self._project) if self._project in projects_list else -1,
            "due_date": self._due_date,
            "items": self._items
        }

    @classmethod
    def from_dict(cls, data, clients_list, projects_list):
        client = clients_list[data["client_idx"]] if 0 <= data["client_idx"] < len(clients_list) else None
        project = projects_list[data["project_idx"]] if 0 <= data["project_idx"] < len(projects_list) else None
        inv = cls(client, project, data["due_date"])
        inv._items = data.get("items", [])
        return inv


class FreelanceManagementSystem:
    def __init__(self):
        self.clients = []
        self.projects = []
        self.invoices = []
        self.data_file = "data.json"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, "r") as f:
                data = json.load(f)
                self.clients = [Client.from_dict(c) for c in data.get("clients", [])]
                self.projects = [Project.from_dict(p) for p in data.get("projects", [])]
                self.invoices = [Invoice.from_dict(i, self.clients, self.projects) for i in data.get("invoices", [])]

    def save_data(self):
        data = {
            "clients": [c.to_dict() for c in self.clients],
            "projects": [p.to_dict() for p in self.projects],
            "invoices": [i.to_dict(self.clients, self.projects) for i in self.invoices]
        }
        with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)

    def start(self):
        while True:
            print("\n" + "="*40)
            print(" FREELANCE MANAGEMENT SYSTEM ")
            print("="*40)
            print("1. Manage Clients")
            print("2. Manage Projects")
            print("3. Manage Invoices")
            print("4. Financial Reports")
            print("5. Exit")
            
            choice = input("Enter choice (1-5): ")
            
            if choice == '1':
                self.manage_clients()
            elif choice == '2':
                self.manage_projects()
            elif choice == '3':
                self.manage_invoices()
            elif choice == '4':
                self.financial_reports()
            elif choice == '5':
                self.save_data()
                print("Data saved. Exiting System.")
                break
            else:
                print("Invalid choice, please try again.")

    def manage_clients(self):
        while True:
            print("\n--- Client Management ---")
            print("1. Add Client")
            print("2. View Clients")
            print("3. Update Client")
            print("4. Delete Client")
            print("5. Back to Main Menu")
            
            choice = input("Enter choice: ")
            if choice == '1':
                name = input("Enter client name: ")
                contact = input("Enter contact info: ")
                terms = input("Enter payment terms: ")
                self.clients.append(Client(name, contact, terms))
                print("Client added successfully.")
            elif choice == '2':
                self.view_clients()
            elif choice == '3':
                self.view_clients()
                if not self.clients: continue   # if no existing clients
                try:
                    idx = int(input("Enter client number to update: ")) - 1
                    if 0 <= idx < len(self.clients):
                        c = self.clients[idx]
                        c.set_name(input(f"Enter new name ({c.get_name()}): ") or c.get_name())
                        c.set_contact(input(f"Enter new contact ({c.get_contact()}): ") or c.get_contact())
                        c.set_payment_terms(input(f"Enter new terms ({c.get_payment_terms()}): ") or c.get_payment_terms())
                        print("Client updated.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '4':
                self.view_clients()
                if not self.clients: continue   # if no existing clients
                try:
                    idx = int(input("Enter client number to delete: ")) - 1
                    if 0 <= idx < len(self.clients):
                        del self.clients[idx]
                        print("Client deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

    def view_clients(self):
        if not self.clients:   # if no existing clients   
            print("No clients found.")
            return
        for i, c in enumerate(self.clients, 1):
            print(f"{i}. {c.display_info()}")

    def manage_projects(self):
        while True:
            print("\n--- Project Management ---")
            print("1. Add Project")
            print("2. View Projects")
            print("3. Update Project")
            print("4. Delete Project")
            print("5. Log Expenses")
            print("6. Back to Main Menu")
            
            choice = input("Enter choice: ")
            if choice == '1':
                title = input("Enter project title: ")
                deadline = input("Enter deadline (YYYY-MM-DD): ")
                try:
                    rate = float(input("Enter rate (number): "))
                    self.projects.append(Project(title, deadline, rate))
                    print("Project added successfully.")
                except ValueError:
                    print("Invalid rate. Project not added.")
            elif choice == '2':
                self.view_projects()
            elif choice == '3':
                self.view_projects()
                if not self.projects: continue   
                try:
                    idx = int(input("Enter project number to update: ")) - 1
                    if 0 <= idx < len(self.projects):
                        p = self.projects[idx]
                        p.set_title(input(f"Enter new title ({p.get_title()}): ") or p.get_title())
                        p.set_deadline(input(f"Enter new deadline ({p.get_deadline()}): ") or p.get_deadline())
                        rate_input = input(f"Enter new rate ({p.get_rate()}): ")
                        if rate_input: p.set_rate(float(rate_input))
                        p.status=input(f"Enter new status ({p.status}): ") or p.status
                        print("Project updated.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter valid numbers.")
            elif choice == '4':
                self.view_projects()
                if not self.projects: continue
                try:
                    idx = int(input("Enter project number to delete: ")) - 1
                    if 0 <= idx < len(self.projects):
                        del self.projects[idx]
                        print("Project deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
                self.view_projects()
                if not self.projects: continue
                try:
                    idx = int(input("Enter project number to log details for: ")) - 1
                    if 0 <= idx < len(self.projects):
                        p = self.projects[idx]
                        expenses_input = input(f"Enter expenses to add (current: {p.expenses}): ")
                        p.expenses += float(expenses_input)
                        print("Project details logged.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter valid numbers.")
            elif choice == '6':
                break
            else:
                print("Invalid choice.")

    def view_projects(self):
        if not self.projects:
            print("No projects found.")
            return
        for i, p in enumerate(self.projects, 1):
            print(f"{i}. {p.display_info()}")

    # --- Invoice Management ---
    def manage_invoices(self):
        while True:
            print("\n--- Invoice Management ---")
            print("1. Create Invoice")
            print("2. View Invoices")
            print("3. Update Invoice Items")
            print("4. Delete Invoice")
            print("5. Back to Main Menu")

            choice = input("Enter choice: ")
            if choice == '1':
                if not self.clients or not self.projects:
                    print("You need at least one client and one project to create an invoice.")
                    continue
                self.view_clients()
                try:
                    c_idx = int(input("Select client number: ")) - 1
                    self.view_projects()
                    p_idx = int(input("Select project number: ")) - 1
                    
                    if 0 <= c_idx < len(self.clients) and 0 <= p_idx < len(self.projects):
                        due_date = input("Enter due date (YYYY-MM-DD): ")
                        inv = Invoice(self.clients[c_idx], self.projects[p_idx], due_date)
                        while True:
                            desc = input("Enter item description (or leave empty to stop): ")
                            if not desc: break
                            amt = float(input("Enter item amount: "))
                            inv.add_item(desc, amt)
                        self.invoices.append(inv)
                        print("Invoice created.")
                    else:
                        print("Invalid client or project selection.")
                except ValueError:
                    print("Invalid input.")
            elif choice == '2':
                self.view_invoices()
            elif choice == '3':
                self.view_invoices()
                if not self.invoices: continue
                try:
                    idx = int(input("Enter invoice number to update: ")) - 1
                    if 0 <= idx < len(self.invoices):
                        inv = self.invoices[idx]
                        print("Current Items:")
                        for item in inv.get_items():
                            print(f"- {item['description']}: ${item['amount']}")
                        
                        action = input("Do you want to clear and re-enter items? (y/n): ").lower()
                        if action == 'y':
                            inv.clear_items()
                            while True:
                                desc = input("Enter item description (or leave empty to stop): ")
                                if not desc: break
                                amt = float(input("Enter item amount: "))
                                inv.add_item(desc, amt)
                            print("Invoice items updated.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input.")
            elif choice == '4':
                self.view_invoices()
                if not self.invoices: continue
                try:
                    idx = int(input("Enter invoice number to delete: ")) - 1
                    if 0 <= idx < len(self.invoices):
                        del self.invoices[idx]
                        print("Invoice deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

    def view_invoices(self):
        if not self.invoices:
            print("No invoices found.")
            return
        for i, inv in enumerate(self.invoices, 1):
            print(f"--- Invoice #{i} ---")
            print(inv.display_info())
            print("-------------------")

    # --- Financial Reports ---
    def financial_reports(self):
        print("\n--- Financial Reports ---")
        if not self.projects:
            print("No projects to report on.")
            return

        total_gross = 0.0
        total_tax = 0.0
        total_expenses = 0.0
        total_net = 0.0

        for p in self.projects:
            gross = p.calculate_gross_earnings()
            tax = p.calculate_estimated_tax()
            net = p.calculate_net_income()
            margin = p.calculate_profit_margin()
            
            print(f"\nProject: {p.get_title()}")
            print(f"  Gross Earnings: ${gross:.2f}")
            print(f"  Estimated Tax:  ${tax:.2f}")
            print(f"  Expenses:       ${p.expenses:.2f}")
            print(f"  Net Income:     ${net:.2f}")
            print(f"  Profit Margin:  {margin:.2f}%")

            total_gross += gross
            total_tax += tax
            total_expenses += p.expenses
            total_net += net

        print("\n" + "-"*30)
        print("OVERALL SUMMARY")
        print(f"Total Gross Earnings: ${total_gross:.2f}")
        print(f"Total Estimated Tax:  ${total_tax:.2f}")
        print(f"Total Expenses:       ${total_expenses:.2f}")
        print(f"Total Net Income:     ${total_net:.2f}")
        overall_margin = (total_net / total_gross * 100) if total_gross > 0 else 0
        print(f"Overall Profit Margin: {overall_margin:.2f}%")
        print("-"*30)


if __name__ == "__main__":
    system = FreelanceManagementSystem()
    system.start()
