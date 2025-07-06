# from cli.auth_menu import console
# from managers import ItemManager, CategoryManager, TransactionManager
# from utils.export_to_csv import export_to_csv
# from tabulate import tabulate
# from rich.console import Console
# from utils.session import UserSession
# import questionary
#
# class InventoryCLI:
#     def __init__(self):
#         self.item_manager = ItemManager()
#         self.category_manager = CategoryManager()
#         self.transaction_manager = TransactionManager()
#         self.console = Console()
#
#     def run(self):
#         while True:
#             console.print()
#             choice = questionary.select(
#                 "📦 Choose an action:",
#                 choices=[
#                     "View Items",
#                     "Add Item",
#                     "Update Item",
#                     "Delete Item",
#                     "Search Items",
#                     "Export Inventory to CSV",
#                     "Buy Item",
#                     "Sell Item",
#                     "Manage Categories",
#                     "Exit"
#                 ]
#             ).ask()
#
#             self.handle_choice(choice)
#
#     def handle_choice(self, choice: str):
#         match choice:
#             case "View Items":
#                 self.view_items()
#             case "Add Item":
#                 self.add_item()
#             case "Update Item":
#                 self.update_item()
#             case "Delete Item":
#                 self.delete_item()
#             case "Search Items":
#                 self.search_items()
#             case "Export Inventory to CSV":
#                 self.export_inventory()
#             case "Buy Item":
#                 self.buy_item()
#             case "Sell Item":
#                 self.sell_item()
#             case "Manage Categories":
#                 self.manage_categories()
#             case "Exit":
#                 self.console.print("👋 Exiting. Stay stocked, stay smart.")
#                 exit()
#             case _:
#                 self.console.print("❌ Invalid choice.")
#
#     def view_items(self):
#         self.item_manager.view_items()
#
#     def add_item(self):
#         name = input("📝 Item Name: ")
#         qty = int(input("🔢 Quantity: "))
#         price = float(input("💵 Price: "))
#         category = input("📁 Category: ")
#         self.item_manager.add_item(name, qty, price, category)
#
#     def update_item(self):
#         item_id = int(input("🔍 Item ID to update: "))
#         new_qty = int(input("🔢 New Quantity: "))
#         new_price = float(input("💵 New Price: "))
#         self.item_manager.update_item(item_id, new_qty, new_price)
#
#     def delete_item(self):
#         item_id = int(input("🗑️ Item ID to delete: "))
#         confirm = input("⚠️ Are you sure? (y/n): ").lower()
#         if confirm == "y":
#             self.item_manager.delete_item(item_id)
#
#     def search_items(self):
#         search_choice = questionary.select(
#             "🔍 Search by:",
#             choices=[
#                 "By Name",
#                 "By Category",
#                 "Low Stock",
#                 "Back"
#             ]
#         ).ask()
#
#         if search_choice == "By Name":
#             keyword = input("Enter name to search: ")
#             items = self.item_manager.search_items_by_name(keyword)
#
#
#         elif search_choice == "By Category":
#             category_name = input("Enter category to search: ").strip()
#             category = self.category_manager.get_category_by_name(category_name)
#             if not category:
#                 self.console.print(f"❌ Category '{category_name}' not found.")
#                 return
#             items = self.item_manager.search_items_by_category_id(category.id)
#
#
#         elif search_choice == "Low Stock":
#             threshold = input("Enter stock threshold (default 5): ")
#             threshold = int(threshold) if threshold else 5
#             items = self.item_manager.get_low_stock_items(threshold)
#
#         else:
#             return
#
#         if items:
#             table = [[i.id, i.name, i.quantity, i.price, i.category, i.added_on.strftime('%Y-%m-%d')] for i in items]
#             self.console.print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Category", "Added On"], tablefmt="grid"))
#         else:
#             self.console.print("🔍 No items found.")
#
#     def export_inventory(self):
#         filename = input("📁 Enter filename (default: inventory_export.csv): ") or "inventory_export.csv"
#         export_to_csv(filename)
#
#     def buy_item(self):
#         try:
#             user = UserSession.get_current_user()
#             if not user:
#                 self.console.print("🚫 You must be logged in to perform this action.")
#                 return
#
#             name = input("🛒 Item to BUY: ").strip()
#             qty = int(input("🔢 Quantity: "))
#             item = self.transaction_manager.buy_item(user.id, name, qty)
#             self.console.print(f"✅ Bought {qty} of [bold]{item.name}[/bold]. New stock: {item.quantity}")
#         except Exception as e:
#             self.console.print(f"❌ {e}")
#
#     def sell_item(self):
#         try:
#             user = UserSession.get_current_user()
#             if not user:
#                 self.console.print("🚫 You must be logged in to perform this action.")
#                 return
#
#             name = input("📤 Item to SELL: ").strip()
#             qty = int(input("🔢 Quantity: "))
#             item = self.transaction_manager.sell_item(user.id, name, qty)
#             self.console.print(f"✅ Sold {qty} of [bold]{item.name}[/bold]. New stock: {item.quantity}")
#         except Exception as e:
#             self.console.print(f"❌ {e}")
#
#     def manage_categories(self):
#         while True:
#             cat_choice = questionary.select(
#                 "📂 Category Manager",
#                 choices=[
#                     "View Categories",
#                     "Add Category",
#                     "Delete Category",
#                     "Back to Main Menu"
#                 ]
#             ).ask()
#
#             if cat_choice == "View Categories":
#                 categories = self.category_manager.list_categories()
#                 if categories:
#                     for c in categories:
#                         self.console.print(f"🗂️ {c.id}: {c.name.title()}")
#                 else:
#                     self.console.print("❌ No categories found.")
#
#             elif cat_choice == "Add Category":
#                 name = input("📝 Category name: ").strip()
#                 self.category_manager.add_category(name)
#
#             elif cat_choice == "Delete Category":
#                 name = input("🗑️ Category name to delete: ").strip()
#                 self.category_manager.delete_category(name)
#
#             elif cat_choice == "Back to Main Menu":
#                 break

from managers import ItemManager, CategoryManager, TransactionManager
from utils.export_to_csv import export_to_csv
from utils.session import UserSession
from tabulate import tabulate
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import questionary
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class InventoryCLI:
    def __init__(self):
        self.item_manager = ItemManager()
        self.category_manager = CategoryManager()
        self.transaction_manager = TransactionManager()
        self.console = Console()

    def run(self):
        while True:
            clear_screen()
            banner = Panel.fit(
                Align.center("[bold cyan]📦 Inventory Control Center[/]", vertical="middle"),
                border_style="green"
            )
            self.console.print(banner, justify="center")

            choice = questionary.select(
                "Choose an action:",
                choices=[
                    "View Items",
                    "Add Item",
                    "Update Item",
                    "Delete Item",
                    "Search Items",
                    "Export Inventory to CSV",
                    "Buy Item",
                    "Sell Item",
                    "Manage Categories",
                    "Exit"
                ]
            ).ask()

            self.handle_choice(choice)

    def handle_choice(self, choice: str):
        match choice:
            case "View Items":
                self.view_items()
            case "Add Item":
                self.add_item()
            case "Update Item":
                self.update_item()
            case "Delete Item":
                self.delete_item()
            case "Search Items":
                self.search_items()
            case "Export Inventory to CSV":
                self.export_inventory()
            case "Buy Item":
                self.buy_item()
            case "Sell Item":
                self.sell_item()
            case "Manage Categories":
                self.manage_categories()
            case "Exit":
                confirm = questionary.confirm("⚠️ Are you sure you want to exit?").ask()
                if confirm:
                    self.console.print("\n👋 [cyan]Goodbye. May your stock never run out.[/cyan]")
                    exit()

    def view_items(self):
        items = self.item_manager.view_items()
        input("\n🔄 Press Enter to return to main menu...")

    def add_item(self):
        name = input("📝 Item Name: ")
        qty = int(input("🔢 Quantity: "))
        price = float(input("💵 Price: "))
        category = input("📁 Category: ")
        self.item_manager.add_item(name, qty, price, category)
        input("\n✅ Item added. Press Enter to return to menu...")

    def update_item(self):
        item_id = int(input("🔍 Item ID to update: "))
        new_qty = int(input("🔢 New Quantity: "))
        new_price = float(input("💵 New Price: "))
        self.item_manager.update_item(item_id, new_qty, new_price)
        input("\n✅ Item updated. Press Enter to return to menu...")

    def delete_item(self):
        item_id = int(input("🗑️ Item ID to delete: "))
        confirm = input("⚠️ Are you sure? (y/n): ").lower()
        if confirm == "y":
            self.item_manager.delete_item(item_id)
        input("\n✅ Done. Press Enter to return to menu...")

    def search_items(self):
        search_choice = questionary.select(
            "🔍 Search by:",
            choices=[
                "By Name",
                "By Category",
                "Low Stock",
                "Back"
            ]
        ).ask()

        if search_choice == "By Name":
            keyword = input("Enter name to search: ")
            items = self.item_manager.search_items_by_name(keyword)

        elif search_choice == "By Category":
            category_name = input("Enter category to search: ").strip()
            category = self.category_manager.get_category_by_name(category_name)
            if not category:
                self.console.print(f"❌ [red]Category '{category_name}' not found.[/red]")
                return
            items = self.item_manager.search_items_by_category_id(category.id)

        elif search_choice == "Low Stock":
            threshold = input("Enter stock threshold (default 5): ")
            threshold = int(threshold) if threshold else 5
            items = self.item_manager.get_low_stock_items(threshold)
        else:
            return

        if items:
            table = [[i.id, i.name, i.quantity, i.price, i.category, i.added_on.strftime('%Y-%m-%d')] for i in items]
            self.console.print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Category", "Added On"], tablefmt="grid"))
        else:
            self.console.print("[yellow]🔍 No items found.[/yellow]")

        input("\n🔄 Press Enter to return to menu...")

    def export_inventory(self):
        filename = input("📁 Enter filename (default: inventory_export.csv): ") or "inventory_export.csv"
        export_to_csv(filename)
        self.console.print(f"✅ [green]Inventory exported to {filename}[/green]")
        input("\n🔄 Press Enter to return to menu...")

    def buy_item(self):
        try:
            user = UserSession.get_current_user()
            if not user:
                self.console.print("[red]🚫 You must be logged in to perform this action.[/red]")
                return

            name = input("🛒 Item to BUY: ").strip()
            qty = int(input("🔢 Quantity: "))
            item = self.transaction_manager.buy_item(user.id, name, qty)
            self.console.print(f"✅ [green]Bought {qty} of [bold]{item.name}[/bold]. New stock: {item.quantity}[/green]")
        except Exception as e:
            self.console.print(f"❌ [red]{e}[/red]")
        input("\n🔄 Press Enter to return to menu...")

    def sell_item(self):
        try:
            user = UserSession.get_current_user()
            if not user:
                self.console.print("[red]🚫 You must be logged in to perform this action.[/red]")
                return

            name = input("📤 Item to SELL: ").strip()
            qty = int(input("🔢 Quantity: "))
            item = self.transaction_manager.sell_item(user.id, name, qty)
            self.console.print(f"✅ [green]Sold {qty} of [bold]{item.name}[/bold]. New stock: {item.quantity}[/green]")
        except Exception as e:
            self.console.print(f"❌ [red]{e}[/red]")
        input("\n🔄 Press Enter to return to menu...")

    def manage_categories(self):
        while True:
            cat_choice = questionary.select(
                "📂 Category Manager",
                choices=[
                    "View Categories",
                    "Add Category",
                    "Delete Category",
                    "Back to Main Menu"
                ]
            ).ask()

            if cat_choice == "View Categories":
                categories = self.category_manager.list_categories()
                if categories:
                    for c in categories:
                        self.console.print(f"🗂️ {c.id}: {c.name.title()}")
                else:
                    self.console.print("[yellow]❌ No categories found.[/yellow]")

            elif cat_choice == "Add Category":
                name = input("📝 Category name: ").strip()
                self.category_manager.add_category(name)

            elif cat_choice == "Delete Category":
                name = input("🗑️ Category name to delete: ").strip()
                self.category_manager.delete_category(name)

            elif cat_choice == "Back to Main Menu":
                break

            input("\n🔄 Press Enter to return to category menu...")
