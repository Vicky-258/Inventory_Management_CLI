from rich.table import Table
from logger import console
from rich.prompt import Prompt, Confirm
from services.DB import get_session
from Models import Items, Categories, Suppliers
from CRUD import create_item, update_item, get_all_suppliers, update_supplier


def prompt_create_item():
    print("\n📦 Add a New Item to Inventory")

    name = input("Enter item name: ").strip()
    if not name:
        print("❌ Item name cannot be empty.")
        return

    description = input("Enter item description (optional): ").strip() or None

    try:
        quantity = int(input("Enter quantity: "))
        if quantity < 0:
            print("❌ Quantity cannot be negative.")
            return
    except ValueError:
        print("❌ Invalid input! Quantity must be a number.")
        return

    try:
        price = float(input("Enter price: "))
        if price < 0:
            print("❌ Price cannot be negative.")
            return
    except ValueError:
        print("❌ Invalid input! Price must be a number.")
        return

    try:
        category_id = int(input("Enter category ID: "))
        supplier_id = int(input("Enter supplier ID: "))
    except ValueError:
        print("❌ Category ID and Supplier ID must be valid numbers.")
        return

    low_stock_threshold = input("Enter low stock threshold (default: 5): ").strip() or "5"
    try:
        low_stock_threshold = int(low_stock_threshold)
        if low_stock_threshold < 0:
            print("❌ Low stock threshold cannot be negative.")
            return
    except ValueError:
        print("❌ Invalid input! Low stock threshold must be a number.")
        return

    # Call create_item with validated inputs
    create_item(name, description, quantity, price, category_id, supplier_id, low_stock_threshold)


def display_search_results(results):
    if not results:
        console.print("[bold red]No matching items found![/bold red] ❌")
        return

    table = Table(title="🔍 Search Results", show_lines=True)

    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Category", style="yellow")
    table.add_column("Supplier", style="blue")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Stock", justify="right", style="red")

    for item in results:
        table.add_row(
            str(item.id),
            item.name,
            item.category.name if item.category else "N/A",
            item.supplier.name if item.supplier else "N/A",
            f"${item.price:.2f}",
            str(item.quantity)
        )

    console.print(table)


def prompt_update_item():
    session = get_session()

    search_name = Prompt.ask("[bold cyan]Enter item name (partial is fine)[/]").strip()
    items = session.query(Items).filter(Items.name.ilike(f"%{search_name}%")).all()

    if not items:
        console.print("[red]No matching items found![/]")
        return

    # Display matching items
    table = Table(title="Matching Items", show_lines=True)
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Name", style="green")
    table.add_column("Quantity", style="yellow", justify="right")
    table.add_column("Price", style="magenta", justify="right")

    for item in items:
        table.add_row(str(item.id), item.name, str(item.quantity), f"${item.price:.2f}")

    console.print(table)

    # Ask a user to pick an item by ID
    item_id = Prompt.ask("[bold cyan]Enter the ID of the item to update[/]").strip()
    if not item_id.isdigit():
        console.print("[red]Invalid ID! Must be a number.[/]")
        return
    item_id = int(item_id)

    item = session.get(Items, item_id)
    if not item:
        console.print("[red]Item not found![/]")
        return

    console.print(f"[bold green]Updating Item:[/] {item.name}")

    updates = {}

    if Confirm.ask("Do you want to update the name?"):
        updates["name"] = Prompt.ask("Enter new name", default=item.name)

    if Confirm.ask("Do you want to update the description?"):
        updates["description"] = Prompt.ask("Enter new description", default=item.description or "")

    if Confirm.ask("Do you want to change the category?"):
        categories = session.query(Categories).all()
        for cat in categories:
            console.print(f"[yellow]{cat.id}[/]: {cat.name}")
        category_id = Prompt.ask("Enter new Category ID")
        if category_id.isdigit() and session.get(Categories, int(category_id)):
            updates["category_id"] = int(category_id)
        else:
            console.print("[red]Invalid category![/]")

    if Confirm.ask("Do you want to change the supplier?"):
        suppliers = session.query(Suppliers).all()
        for sup in suppliers:
            console.print(f"[yellow]{sup.id}[/]: {sup.name}")
        supplier_id = Prompt.ask("Enter new Supplier ID")
        if supplier_id.isdigit() and session.get(Suppliers, int(supplier_id)):
            updates["supplier_id"] = int(supplier_id)
        else:
            console.print("[red]Invalid supplier![/]")

    if Confirm.ask("Do you want to update the quantity?"):
        quantity = Prompt.ask("Enter new quantity", default=str(item.quantity))
        if quantity.isdigit():
            updates["quantity"] = int(quantity)
        else:
            console.print("[red]Invalid quantity! Must be a number.[/]")

    if Confirm.ask("Do you want to update the price?"):
        price = Prompt.ask("Enter new price", default=f"{item.price:.2f}")
        try:
            updates["price"] = float(price)
        except ValueError:
            console.print("[red]Invalid price! Must be a number.[/]")

    if not updates:
        console.print("[yellow]No changes made.[/]")
        return

    update_item(item_id, **updates)


def display_categories(categories):
    if not categories:
        console.print("[yellow]No categories available.[/]")
        return

    table = Table(title="Categories", show_lines=True)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")

    for category in categories:
        table.add_row(str(category.id), category.name)

    console.print(table)


def display_suppliers(suppliers):
    if not suppliers:
        console.print("[yellow]No suppliers available.[/]")
        return

    table = Table(title="Suppliers", show_lines=True)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Phone", style="blue")

    for supplier in suppliers:
        table.add_row(str(supplier.id), supplier.name, supplier.email, supplier.phone)

    console.print(table)


def prompt_update_supplier():
    suppliers = get_all_suppliers()

    if not suppliers:
        console.print("[yellow]No suppliers available to update.[/]")
        return

    console.print("\n[cyan]Existing Suppliers:[/]")
    display_suppliers(suppliers)  # Assuming we have a function to display suppliers in a table

    supplier_id = Prompt.ask("[blue]Enter Supplier ID to update[/]", default="").strip()
    if not supplier_id.isdigit():
        console.print("[red]Invalid ID! Please enter a number.[/]")
        return

    supplier_id = int(supplier_id)

    name = Prompt.ask("[blue]Enter new name (leave blank to keep unchanged)[/]", default="").strip() or None
    email = Prompt.ask("[blue]Enter new email (leave blank to keep unchanged)[/]", default="").strip() or None
    phone = Prompt.ask("[blue]Enter new phone (leave blank to keep unchanged)[/]", default="").strip() or None

    update_supplier(supplier_id, name, email, phone)

def main():
    pass


if __name__ == "__main__":
    main()
