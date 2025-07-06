from managers import ItemManager, CategoryManager, TransactionManager
from utils.export_to_csv import export_to_csv
from tabulate import tabulate
from rich.console import Console
from utils.session import UserSession
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class InventoryCLI:
    def __init__(self):
        self.item_manager = ItemManager()
        self.category_manager = CategoryManager()
        self.transaction_manager = TransactionManager()
        self.console = Console()

    def run(self):
        while True:
            main_menu = WordCompleter([
                "View Items", "Add Item", "Update Item", "Delete Item",
                "Search Items", "Export Inventory to CSV", "Buy Item",
                "Sell Item", "Manage Categories", "Exit"
            ], ignore_case=True)

            choice = prompt("📦 Select Action: ", completer=main_menu).strip().lower()
            self.handle_choice(choice)

    def handle_choice(self, choice: str):
        choice = choice.lower()
        if "view" in choice:
            self.view_items()
        elif "add" in choice:
            self.add_item()
        elif "update" in choice:
            self.update_item()
        elif "delete" in choice and "category" not in choice:
            self.delete_item()
        elif "search" in choice:
            self.search_items()
        elif "export" in choice:
            self.export_inventory()
        elif "buy" in choice:
            self.buy_item()
        elif "sell" in choice:
            self.sell_item()
        elif "manage" in choice:
            self.manage_categories()
        elif "exit" in choice:
            self.console.print("👋 Exiting. Stay stocked, stay smart.")
            exit()

    def view_items(self):
        self.item_manager.list()

    def add_item(self):
        name = prompt("📝 Item Name: ")
        qty = int(prompt("🔢 Quantity: "))
        price = float(prompt("💵 Price: "))
        category = prompt("📁 Category: ")
        self.item_manager.add(name, qty, price, category)

    def update_item(self):
        item_id = int(prompt("🔍 Item ID to update: "))
        new_qty = int(prompt("🔢 New Quantity: "))
        new_price = float(prompt("💵 New Price: "))
        self.item_manager.update(item_id, new_qty, new_price)

    def delete_item(self):
        item_id = int(prompt("🗑️ Item ID to delete: "))
        confirm = prompt("⚠️ Are you sure? (y/n): ").lower()
        if confirm == "y":
            self.item_manager.delete(item_id)

    def search_items(self):
        search_choice = radiolist_dialog(
            title="🔍 Search Menu",
            text="Search by:",
            values=[
                ("1", "By Name"),
                ("2", "By Category"),
                ("3", "Low Stock"),
                ("4", "Back")
            ]
        ).run()

        if search_choice == "1":
            keyword = prompt("Enter name to search: ")
            items = self.item_manager.search_items_by_name(keyword)
        elif search_choice == "2":
            category_name = input("Enter category to search: ").strip()
            category = self.category_manager.get_category_by_name(category_name)
            if not category:
                self.console.print(f"❌ Category '{category_name}' not found.")
                return
            items = self.item_manager.search_items_by_category_id(category.id)
        elif search_choice == "3":
            threshold = prompt("Enter stock threshold (default 5): ")
            threshold = int(threshold) if threshold else 5
            items = self.item_manager.get_low_stock_items(threshold)
        else:
            return

        if items:
            table = [[i.id, i.name, i.quantity, i.price, i.category, i.added_on.strftime('%Y-%m-%d')] for i in items]
            self.console.print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Category", "Added On"], tablefmt="grid"))
        else:
            self.console.print("🔍 No items found.")

    def export_inventory(self):
        filename = prompt("📁 Enter filename (default: inventory_export.csv): ") or "inventory_export.csv"
        export_to_csv(filename)

    def buy_item(self):
        try:
            user = UserSession.get_current_user()
            if not user:
                self.console.print("🚫 You must be logged in to perform this action.")
                return

            name = prompt("🛒 Item to BUY: ").strip()
            qty = int(prompt("🔢 Quantity: "))
            item = self.transaction_manager.buy_item(user.id, name, qty)
            self.console.print(f"✅ Bought {qty} of [bold]{item.name}[/bold]. New stock: {item.quantity}")
        except Exception as e:
            self.console.print(f"❌ {e}")

    def sell_item(self):
        try:
            user = UserSession.get_current_user()
            if not user:
                self.console.print("🚫 You must be logged in to perform this action.")
                return

            name = prompt("📤 Item to SELL: ").strip()
            qty = int(prompt("🔢 Quantity: "))
            item = self.transaction_manager.sell_item(user.id, name, qty)
            self.console.print(f"✅ Sold {qty} of [bold]{item.name}[/bold]. New stock: {item.quantity}")
        except Exception as e:
            self.console.print(f"❌ {e}")

    def manage_categories(self):
        while True:
            cat_choice = radiolist_dialog(
                title="📂 Category Manager",
                text="Choose an action:",
                values=[
                    ("1", "View Categories"),
                    ("2", "Add Category"),
                    ("3", "Delete Category"),
                    ("4", "Back")
                ]
            ).run()

            if cat_choice == "1":
                categories = self.category_manager.list()
                if categories:
                    for c in categories:
                        self.console.print(f"🗂️ {c.id}: {c.name.title()}")
                else:
                    self.console.print("❌ No categories found.")

            elif cat_choice == "2":
                name = prompt("📝 Category name: ").strip()
                self.category_manager.add(name)

            elif cat_choice == "3":
                name = prompt("🗑️ Category name to delete: ").strip()
                self.category_manager.delete(name)

            elif cat_choice == "4":
                break
