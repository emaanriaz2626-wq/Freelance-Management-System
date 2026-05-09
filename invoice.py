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