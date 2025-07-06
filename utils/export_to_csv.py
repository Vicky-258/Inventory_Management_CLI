import csv
from db import get_db
from models import Item
from sqlalchemy.orm import joinedload

def export_to_csv(filename="inventory_export.csv"):
    with get_db() as db:
        items = db.query(Item).options(joinedload(Item.category)).all()

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
                item.category.name if item.category else "Uncategorized",
                item.added_on.strftime('%Y-%m-%d %H:%M:%S')
            ])

    print(f"✅ Inventory exported to {filename}")
