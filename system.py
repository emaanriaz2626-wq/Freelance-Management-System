import os
import json
import pandas as pd

from client import Client
from project import Project
from invoice import Invoice
from graphs import GraphManager
from currency import CurrencyScraper

class FreelanceManagementSystem:
    def __init__(self):
        self.clients = []
        self.projects = []
        self.invoices = []
        self.data_file = "data.json"
        self.load_data()

    def load_data(self):
        #check file exists
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, "r") as f:
                data = json.load(f)
                self.clients = [Client.from_dict(c) for c in data.get("clients", [])]
                self.projects = [Project.from_dict(p) for p in data.get("projects", [])]
                self.invoices = [Invoice.from_dict(i, self.clients, self.projects) for i in data.get("invoices", [])]

    def save_data(self):
        #prepare data dict
        data = {
            "clients": [c.to_dict() for c in self.clients],
            "projects": [p.to_dict() for p in self.projects],
            "invoices": [i.to_dict(self.clients, self.projects) for i in self.invoices]
        }
        with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)

    def start(self):
        #main menu loop
        while True:
            print("\n" + "="*40)
            print(" FREELANCE MANAGEMENT SYSTEM ")
            print("="*40)
            print("1. Manage Clients")
            print("2. Manage Projects")
            print("3. Manage Invoices")
            print("4. Financial Reports")
            print("5. Project Status Chart")
            print("6. Exit")
            
            choice = input("Enter choice (1-6): ")
            
            if choice == '1':
                self.manage_clients()
            elif choice == '2':
                self.manage_projects()
            elif choice == '3':
                self.manage_invoices()
            elif choice == '4':
                self.financial_reports()
            elif choice == '5':
                GraphManager.plot_project_status(self.projects)
            elif choice == '6':
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
                #add new client
                name = input("Enter client name: ")
                contact = input("Enter contact info: ")
                terms = input("Enter payment terms: ")
                currency = input("Enter currency name (e.g., US Dollar, Euro) [US Dollar]: ").strip().title() or "US Dollar"
                self.clients.append(Client(name, contact, terms, currency))
                print("Client added successfully.")
            elif choice == '2':
                self.view_clients()
            elif choice == '3':
                self.view_clients()
                if not self.clients: continue   #if no clients
                try:
                    #update client info
                    idx = int(input("Enter client number to update: ")) - 1
                    if 0 <= idx < len(self.clients):
                        c = self.clients[idx]
                        c.set_name(input(f"Enter new name ({c.get_name()}): ") or c.get_name())
                        c.set_contact(input(f"Enter new contact ({c.get_contact()}): ") or c.get_contact())
                        c.set_payment_terms(input(f"Enter new terms ({c.get_payment_terms()}): ") or c.get_payment_terms())
                        c.set_currency(input(f"Enter new currency name ({c.currency}): ").strip().title() or c.currency)
                        print("Client updated.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '4':
                self.view_clients()
                if not self.clients: continue   #if no clients
                try:
                    #delete client
                    idx = int(input("Enter client number to delete: ")) - 1
                    if 0 <= idx < len(self.clients):
                        client_to_delete = self.clients[idx]
                        #remove client invoices
                        self.invoices = [inv for inv in self.invoices if inv.get_client() != client_to_delete]
                        del self.clients[idx]
                        print("Client and associated invoices deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

    def view_clients(self):
        if not self.clients:   #if no clients   
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
            print("5. Log Expenses/Hours Worked")
            print("6. Project Financial Breakdown")
            print("7. Back to Main Menu")
            
            choice = input("Enter choice: ")
            if choice == '1':
                #add new project
                title = input("Enter project title: ")
                deadline = input("Enter deadline (YYYY-MM-DD): ")
                try:
                    rate = float(input("Enter rate (number): "))
                    rate_type = input("Enter rate type (f=fixed / h=hourly): ").lower()
                    if rate_type not in ["f", "h"]:
                        print("Invalid rate type. Project not added.")
                        continue
                    self.projects.append(Project(title, deadline, rate, rate_type))
                    print("Project added successfully.")
                except ValueError:
                    print("Invalid rate. Project not added.")
            elif choice == '2':
                self.view_projects()
            elif choice == '3':
                self.view_projects()
                if not self.projects: continue   
                try:
                    #update project info
                    idx = int(input("Enter project number to update: ")) - 1
                    if 0 <= idx < len(self.projects):
                        p = self.projects[idx]
                        p.set_title(input(f"Enter new title ({p.get_title()}): ") or p.get_title())
                        p.set_deadline(input(f"Enter new deadline ({p.get_deadline()}): ") or p.get_deadline())
                        rate_input = input(f"Enter new rate ({p.get_rate()}): ")
                        if rate_input: p.set_rate(float(rate_input))
                        p.status=input(f"Enter new status ({p.status}): ") or p.status
                        
                        hw_input = input(f"Enter new hours worked ({p.hours_worked}): ")
                        if hw_input: p.hours_worked = float(hw_input)
                        
                        p.rate_type = input(f"Enter new rate type ({p.rate_type}): ") or p.rate_type
                        print("Project updated.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter valid numbers.")
            elif choice == '4':
                self.view_projects()
                if not self.projects: continue
                try:
                    #delete project
                    idx = int(input("Enter project number to delete: ")) - 1
                    if 0 <= idx < len(self.projects):
                        project_to_delete = self.projects[idx]
                        #remove project invoices
                        self.invoices = [inv for inv in self.invoices if inv.get_project() != project_to_delete]
                        del self.projects[idx]
                        print("Project and associated invoices deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
                self.view_projects()
                if not self.projects: continue
                try:
                    #log project details
                    idx = int(input("Enter project number to log details for: ")) - 1
                    if 0 <= idx < len(self.projects):
                        p = self.projects[idx]
                        expenses_input = input(f"Enter expenses to add (current: {p.expenses}): ")
                        if expenses_input: p.expenses += float(expenses_input)
                        
                        hours_input = input(f"Enter hours worked to add (current: {p.hours_worked}): ")
                        if hours_input: p.hours_worked += float(hours_input)
                        
                        print("Project details logged.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter valid numbers.")
            elif choice == '6':
                GraphManager.plot_financial_breakdown(self.projects)
            elif choice == '7':
                break
            else:
                print("Invalid choice.")

    def view_projects(self):
        if not self.projects:
            print("No projects found.")
            return
        for i, p in enumerate(self.projects, 1):
            print(f"{i}. {p.display_info()}")

    def manage_invoices(self):
        while True:
            print("\n--- Invoice Management ---")
            print("1. Create Invoice")
            print("2. View Invoices")
            print("3. Update Invoice Items")
            print("4. View Invoice in Client Currency")
            print("5. Delete Invoice")
            print("6. Back to Main Menu")

            choice = input("Enter choice: ")
            if choice == '1':
                #check requirements
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
                    idx = int(input("Enter invoice number to view in client's currency: ")) - 1
                    if 0 <= idx < len(self.invoices):
                        inv = self.invoices[idx]
                        client = inv.get_client()
                        target_currency = client.currency
                        total_usd = inv.get_totals()
                        
                        if target_currency.lower() in ["usd", "us dollar", "1.00 usd"]:
                            print(f"Client's currency is already US Dollar. Total: ${total_usd:.2f}")
                        else:
                            print(f"Fetching live exchange rate for US Dollar to {target_currency}...")
                            rate = CurrencyScraper.get_exchange_rate("US Dollar", target_currency)
                            if rate:
                                total_converted = total_usd * rate
                                print(f"Exchange Rate: 1 USD = {rate} {target_currency}")
                                print(f"Invoice Total ({target_currency}): {total_converted:.2f} {target_currency}")
                            else:
                                print("Failed to fetch exchange rate.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '5':
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
            elif choice == '6':
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

    #financial reports
    def financial_reports(self):
        print("\n--- Financial Reports ---")
        if not self.projects:
            print("No projects to report on.")
            return

        data = []
        for p in self.projects:
            gross = p.calculate_gross_earnings()
            tax = p.calculate_estimated_tax()
            net = p.calculate_net_income()
            margin = p.calculate_profit_margin()
            
            data.append({
                "Project Title": p.get_title(),
                "Gross Earnings": gross,
                "Estimated Tax": tax,
                "Expenses": p.expenses,
                "Net Income": net,
                "Profit Margin (%)": margin
            })

        df = pd.DataFrame(data)

        #display report
        print("\nDetailed Project Report:")
        pd.set_option('display.float_format', '{:.2f}'.format)
        print(df.to_string())

        #calculate summary
        print("\n" + "-" * 30)
        print("OVERALL SUMMARY")
        total_gross = df["Gross Earnings"].sum()
        total_tax = df["Estimated Tax"].sum()
        total_expenses = df["Expenses"].sum()
        total_net = df["Net Income"].sum()

        print(f"Total Gross Earnings: ${total_gross:.2f}")
        print(f"Total Estimated Tax:  ${total_tax:.2f}")
        print(f"Total Expenses:       ${total_expenses:.2f}")
        print(f"Total Net Income:     ${total_net:.2f}")
        overall_margin = (total_net / total_gross * 100) if total_gross > 0 else 0
        print(f"Overall Profit Margin: {overall_margin:.2f}%")

        #provide summary stats
        print("\nSummary Statistics (mean, min, max):")
        stats_df = df[["Gross Earnings", "Estimated Tax", "Expenses", "Net Income", "Profit Margin (%)"]].describe()
        print(stats_df.loc[['mean', 'min', 'max']])
        print("-" * 30)
