from db import Base, engine
from CRUD import add_item, view_items, update_item, delete_item, search_items_by_name, search_items_by_category, get_low_stock_items
from tabulate import tabulate
from utils import export_to_csv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_banner():
    banner_text = Text("📦 Inventory CLI", justify="center", style="bold magenta")
    console.print(Panel(banner_text, expand=True, border_style="cyan"))

def init_db():
    Base.metadata.create_all(engine)


def menu():
    console.print("\n🧾 [bold underline cyan]Inventory Menu[/bold underline cyan]")
    menu_items = [
        "1. View Items",
        "2. Add Item",
        "3. Update Item",
        "4. Delete Item",
        "5. Search Items",
        "6. Export Inventory to CSV",
        "7. Exit"
    ]
    for item in menu_items:
        console.print(f"[green]»[/green] {item}")

def main():
    init_db()
    while True:
        menu()
        choice = input("➡️ Enter choice (1-7): ").strip()

        if choice == "1":
            view_items()

        elif choice == "2":
            print()
            name = input("📝 Item Name: ")
            qty = int(input("🔢 Quantity: "))
            price = float(input("💵 Price: "))
            category = input("Category: ")
            print()
            add_item(name, qty, price, category)

        elif choice == "3":
            item_id = int(input("🔍 Item ID to update: "))
            new_qty = int(input("🔢 New Quantity: "))
            new_price = float(input("💵 New Price: "))
            update_item(item_id, new_qty, new_price)

        elif choice == "4":
            item_id = int(input("🗑️ Item ID to delete: "))
            confirm = input("⚠️ Are you sure? (y/n): ").lower()
            if confirm == "y":
                delete_item(item_id)


        elif choice == "5":

            console.print("\n🔍 Search Menu")
            console.print("1. By Name")
            console.print("2. By Category")
            console.print("3. Low Stock (qty < 5)")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":

                keyword = input("Enter name to search: ")
                items = search_items_by_name(keyword)


            elif sub_choice == "2":

                category = input("Enter category to search: ")
                items = search_items_by_category(category)


            elif sub_choice == "3":

                threshold = input("Enter stock threshold (default 5): ")
                threshold = int(threshold) if threshold else 5
                items = get_low_stock_items(threshold)

            else:
                console.print("⚠️ Invalid choice.")
                items = []

            if items:
                table = [[i.id, i.name, i.quantity, i.price, i.category, i.added_on.strftime('%Y-%m-%d')] for i in
                         items]
                console.print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Category", "Added On"], tablefmt="grid"))
            else:
                console.print("🔍 No items found.")

        elif choice == "6":
            filename = input("📁 Enter filename (default: inventory_export.csv): ") or "inventory_export.csv"
            export_to_csv(filename)

        elif choice == "7":
            console.print("👋 Exiting. Stay stocked, stay smart.")
            break

        else:
            console.print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    print_banner()
    main()
