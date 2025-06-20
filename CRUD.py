from models import Item
from db import Session
from tabulate import tabulate

def add_item(name, quantity, price, category="Uncategorized"):
    session = Session()
    item = Item(name=name, quantity=quantity, price=price, category=category)
    session.add(item)
    session.commit()
    session.close()
    print(f"✅ Added '{name}' to inventory under '{category}' category.")


def view_items():
    session = Session()
    items = session.query(Item).all()
    session.close()

    if not items:
        print("📦 Inventory is empty.")
        return

    table = [[item.id, item.name, item.quantity, item.price, item.category, item.added_on.strftime('%Y-%m-%d') ] for item in items]
    print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Category", "Added On"], tablefmt="grid"))

    # 🔔 Low stock warning
    for item in items:
        if item.quantity < 5:
            print(f"🚨 LOW STOCK: '{item.name}' only has {item.quantity} units left!")

def update_item(item_id, new_qty, new_price):
    session = Session()
    item = session.query(Item).get(item_id)
    if item:
        item.quantity = new_qty
        item.price = new_price
        session.commit()
        print(f"✅ Updated '{item.name}'.")
    else:
        print("❌ Item not found.")
    session.close()

def delete_item(item_id):
    session = Session()
    item = session.query(Item).get(item_id)
    if item:
        session.delete(item)
        session.commit()
        print(f"🗑️ Deleted '{item.name}'.")
    else:
        print("❌ Item not found.")
    session.close()

def search_items_by_name(keyword):
    session = Session()
    items = session.query(Item).filter(Item.name.ilike(f"%{keyword}%")).all()
    session.close()
    return items

def search_items_by_category(category):
    session = Session()
    items = session.query(Item).filter(Item.category.ilike(f"%{category}%")).all()
    session.close()
    return items

def get_low_stock_items(threshold=5):
    session = Session()
    items = session.query(Item).filter(Item.quantity < threshold).all()
    session.close()
    return items

