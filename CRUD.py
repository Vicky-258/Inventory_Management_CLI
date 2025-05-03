from sqlalchemy import func
from Models import Items, Categories, Suppliers
from services.DB import get_session
from sqlalchemy.orm import joinedload
from logger import console
from rich import prompt
import re

def create_item(name: str, description: str, quantity: int, price: float, category_id, supplier_id, low_stock_threshold=5):
    session = get_session()

    try:
        # Basic validation
        if not name.strip():
            raise ValueError("Item name cannot be empty.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(category_id, int) or not isinstance(supplier_id, int):
            raise ValueError("Category ID and Supplier ID must be integers.")
        if low_stock_threshold < 0:
            raise ValueError("Low stock threshold cannot be negative.")

        # Create and save item
        new_item = Items(
            name=name.strip(),
            description=description.strip() if description else None,
            quantity=quantity,
            price=price,
            category_id=category_id,
            supplier_id=supplier_id,
            low_stock_threshold=low_stock_threshold
        )
        session.add(new_item)
        session.commit()
        print(f"✅ Item '{name}' added successfully!")

    except ValueError as ve:
        print(f"❌ Validation Error: {ve}")
        session.rollback()
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_items():
    session = get_session()
    items = session.query(Items).all()
    if items:
        session.close()
        return items
    else:
        session.close()
        raise ValueError("No items found!")


def search_products(name=None, category=None, supplier=None, low_stock=False):
    session = get_session()

    # Using joinedload for performance & reducing extra queries
    query = session.query(Items).options(
        joinedload(Items.category),
        joinedload(Items.supplier)
    )

    if name:
        query = query.filter(Items.name.ilike(f"%{name}%"))  # Partial case-insensitive match

    if category:
        query = query.join(Categories).filter(Categories.name.ilike(f"%{category}%"))

    if supplier:
        query = query.join(Suppliers).filter(Suppliers.name.ilike(f"%{supplier}%"))

    if low_stock:
        query = query.filter(Items.quantity <= Items.low_stock_threshold)

    results = query.all()

    if not results:
        return []

    return results


def update_item(item_id, name=None, description=None, category_id=None, supplier_id=None, quantity=None, price=None):
    session = get_session()
    item = session.get(Items, item_id)

    if not item:
        console.print("[red]Error:[/] Item not found!")
        return

    updated_fields = []

    if name:
        item.name = name
        updated_fields.append(f"Name: {name}")

    if description:
        item.description = description
        updated_fields.append(f"Description: {description}")

    if category_id:
        category = session.get(Categories, category_id)
        if not category:
            console.print("[red]Error:[/] Invalid category ID!")
            return
        item.category_id = category_id
        updated_fields.append(f"Category: {category.name}")

    if supplier_id:
        supplier = session.get(Suppliers, supplier_id)
        if not supplier:
            console.print("[red]Error:[/] Invalid supplier ID!")
            return
        item.supplier_id = supplier_id
        updated_fields.append(f"Supplier: {supplier.name}")

    if quantity is not None:
        if quantity < 0:
            console.print("[red]Error:[/] Quantity cannot be negative!")
            return
        item.quantity = quantity
        updated_fields.append(f"Quantity: {quantity}")

    if price is not None:
        if price <= 0:
            console.print("[red]Error:[/] Price must be greater than 0!")
            return
        item.price = price
        updated_fields.append(f"Price: {price:.2f}")

    if not updated_fields:
        console.print("[yellow]No changes were made.[/]")
        return

    session.commit()
    session.close()

    console.print(f"[green]Successfully updated item![/] {', '.join(updated_fields)}")


def delete_item(item_identifier):
    session = get_session()

    # Try to find the item by ID or name
    item = session.get(Items, item_identifier) if isinstance(item_identifier, int) else \
           session.query(Items).filter(Items.name.ilike(f"%{item_identifier}%")).first()

    if not item:
        console.print("[red]Error:[/] Item not found!")
        return

    # Confirmation prompt before deleting
    confirm = prompt.Confirm.ask(f"Are you sure you want to delete [yellow]{item.name}[/]?")
    if not confirm:
        console.print("[yellow]Deletion cancelled.[/]")
        return

    session.delete(item)
    session.commit()
    session.close()

    console.print(f"[green]Successfully deleted:[/] {item.name}")


def create_category(name):
    session = get_session()

    # Validate input
    name = name.strip()
    if not name:
        console.print("[red]Error:[/] Category name cannot be empty!")
        return

    # Check if category already exists (case-insensitive)
    existing = session.query(Categories).filter(func.lower(Categories.name) == name.lower()).first()
    if existing:
        console.print(f"[yellow]Warning:[/] Category '{name}' already exists!")
        return

    # Create new category
    new_category = Categories(name=name)
    session.add(new_category)
    session.commit()
    session.close()

    console.print(f"[green]Category '{name}' created successfully![/]")


def get_all_categories():
    """Fetch all categories from the database and return them."""
    session = get_session()
    try:
        categories = session.query(Categories).all()
        return categories if categories else None
    except Exception as e:
        console.print(f"[red]Error retrieving categories:[/] {e}")
        return None
    finally:
        session.close()


def update_category(category_id, name):
    session = get_session()
    category = session.get(Categories, category_id)

    if not category:
        console.print("[red]Error:[/] Category not found!")
        return

    if not name.strip():
        console.print("[red]Error:[/] Category name cannot be empty!")
        return

    category.name = name.strip()
    session.commit()
    session.close()

    console.print(f"[green]Category updated successfully![/] New name: [bold]{name}[/]")


def delete_category(category_id):
    session = get_session()
    category = session.get(Categories, category_id)

    if not category:
        console.print("[red]Error:[/] Category not found!")
        return

    # Check if items are linked to this category
    linked_items = session.query(Items).filter_by(category_id=category_id).count()
    if linked_items > 0:
        console.print(f"[yellow]Warning:[/] This category has {linked_items} linked item(s). Consider reassigning them before deleting.")
        return

    session.delete(category)
    session.commit()
    session.close()

    console.print(f"[green]Category deleted successfully![/] (ID: {category_id})")


def create_supplier(name, email, phone):
    session = get_session()

    # Check for existing supplier with the same name or email
    existing_supplier = session.query(Suppliers).filter(
        (Suppliers.name == name) | (Suppliers.email == email)
    ).first()

    if existing_supplier:
        console.print("[red]Error:[/] Supplier with this name or email already exists!")
        return

    # Validate email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        console.print("[red]Error:[/] Invalid email format!")
        return

    # Validate phone number (basic check)
    if not phone.isdigit() or len(phone) < 7:
        console.print("[red]Error:[/] Invalid phone number!")
        return

    # Create the supplier
    new_supplier = Suppliers(name=name, email=email, phone=phone)
    session.add(new_supplier)
    session.commit()
    session.close()

    console.print(f"[green]Supplier '{name}' added successfully![/]")


def get_all_suppliers():
    """Fetch all suppliers from the database and return them as a list."""
    session = get_session()
    try:
        suppliers = session.query(Suppliers).all()
        return suppliers if suppliers else None
    except Exception as e:
        console.print(f"[red]Error retrieving suppliers:[/] {e}")
        return None
    finally:
        session.close()


def update_supplier(supplier_id, name=None, email=None, phone=None):
    session = get_session()
    supplier = session.get(Suppliers, supplier_id)

    if not supplier:
        console.print("[red]Error:[/] Supplier not found!")
        return

    updated_fields = []

    if name:
        supplier.name = name
        updated_fields.append(f"Name: {name}")

    if email:
        supplier.email = email
        updated_fields.append(f"Email: {email}")

    if phone:
        supplier.phone = phone
        updated_fields.append(f"Phone: {phone}")

    if not updated_fields:
        console.print("[yellow]No changes were made.[/]")
        return

    session.commit()
    session.close()

    console.print(f"[green]Successfully updated supplier![/] {', '.join(updated_fields)}")


def main():

    print(search_products())

if __name__ == '__main__':
    main()