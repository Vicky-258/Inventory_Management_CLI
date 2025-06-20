import csv
from db import Session
from models import Item

def export_to_csv(filename="inventory_export.csv"):
    session = Session()
    items = session.query(Item).all()
    session.close()

    if not items:
        print("📦 Inventory is empty. Nothing to export.")
        return

    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Price", "Category", "Added On"])
        for item in items:
            writer.writerow([
                item.id,
                item.name,
                item.quantity,
                item.price,
                item.category,
                item.added_on.strftime('%Y-%m-%d %H:%M:%S')
            ])
    print(f"✅ Inventory exported to {filename}")
