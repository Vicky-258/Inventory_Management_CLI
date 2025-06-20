from db import Base, engine
from models import Item
from CRUD import add_item, view_items, update_item, delete_item


def init_db():
    Base.metadata.create_all(engine)


def menu():
    print("\n🛒 WAREHOUSE INVENTORY MANAGER")
    print("1. View all items")
    print("2. Add new item")
    print("3. Update existing item")
    print("4. Delete item")
    print("5. Exit")


def main():
    init_db()
    while True:
        menu()
        choice = input("➡️ Enter choice (1-5): ").strip()

        if choice == "1":
            view_items()

        elif choice == "2":
            name = input("📝 Item Name: ")
            qty = int(input("🔢 Quantity: "))
            price = float(input("💵 Price: "))
            add_item(name, qty, price)

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
            print("👋 Exiting. Stay stocked, stay smart.")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
