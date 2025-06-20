from models import Item
from db import Session
from tabulate import tabulate

def add_item(name, quantity, price):
    session = Session()
    item = Item(name=name, quantity=quantity, price=price)
    session.add(item)
    session.commit()
    session.close()
    print(f"✅ Added '{name}' to inventory!")

def view_items():
    session = Session()
    items = session.query(Item).all()
    session.close()

    if not items:
        print("📭 Inventory is empty.")
        return

    table = [[i.id, i.name, i.quantity, i.price, i.added_on.strftime("%Y-%m-%d %H:%M")] for i in items]
    print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Added On"], tablefmt="fancy_grid"))

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
