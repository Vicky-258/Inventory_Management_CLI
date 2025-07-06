from models import Item
from db import get_db
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from models import Category
from tabulate import tabulate
from rich.console import Console
from difflib import get_close_matches
from sqlalchemy.orm import joinedload

console = Console()


class ItemManager:
    def add_item(self, name, quantity, price, category_name="Uncategorized"):
        with get_db() as session:
            try:
                normalized_name = category_name.lower()
                category = session.query(Category).filter(Category.name.ilike(normalized_name)).first()

                if not category:
                    all_categories = [c.name for c in session.query(Category).all()]
                    suggestions = get_close_matches(normalized_name, all_categories, n=3, cutoff=0.6)

                    if suggestions:
                        print(f"❓ Category '{category_name}' not found. Did you mean:")
                        for i, suggestion in enumerate(suggestions, 1):
                            print(f"   {i}. {suggestion}")
                        print("   0. Create a new category instead")

                        choice = input("➡️ Enter your choice number (or 0 to create new): ").strip()
                        if choice.isdigit():
                            choice = int(choice)
                            if choice == 0:
                                pass
                            elif 1 <= choice <= len(suggestions):
                                normalized_name = suggestions[choice - 1].lower()
                                category = session.query(Category).filter(Category.name.ilike(normalized_name)).first()
                            else:
                                print("❌ Invalid choice.")
                                return
                        else:
                            print("❌ Invalid input.")
                            return

                    if not category:
                        confirm = input(f"➕ Create new category '{category_name}'? (y/n): ").lower()
                        if confirm == "y":
                            category = Category(name=normalized_name)
                            session.add(category)
                            session.commit()
                            print(f"✅ Created new category '{normalized_name}'.")
                        else:
                            print("❌ Aborted item addition.")
                            return

                item = Item(name=name.lower(), quantity=quantity, price=price, category_id=category.id)
                session.add(item)
                session.commit()
                print(f"✅ Added '{name}' under category '{category.name}'.")

            except SQLAlchemyError as e:
                session.rollback()
                print(f"❌ Error adding item: {e}")

    def view_items(self):
        with get_db() as db:
            items: List[Item] = db.query(Item).all()

            if not items:
                console.print("📦 Inventory is empty.")
                return

            table = [[item.id, item.name.title(), item.quantity, item.price, item.category, item.added_on.strftime('%Y-%m-%d')]
                     for item in items]

            console.print(tabulate(table, headers=["ID", "Name", "Qty", "Price", "Category", "Added On"], tablefmt="grid"))

            for item in items:
                if item.quantity < 5:
                    console.print(f"🚨 LOW STOCK: '[bold red]{item.name}[/bold red]' only has {item.quantity} units left!")

    def update_item(self, item_id: int, new_qty: int, new_price: float):
        with get_db() as db:
            item = db.query(Item).get(item_id)
            if item:
                item.quantity = new_qty
                item.price = new_price
                db.commit()
                console.print(f"✅ Updated '[bold]{item.name}[/bold]'.")
            else:
                console.print("❌ Item not found.")

    def delete_item(self, item_id: int):
        with get_db() as db:
            item = db.query(Item).get(item_id)
            if item:
                db.delete(item)
                db.commit()
                console.print(f"🗑️ Deleted '[bold]{item.name}[/bold]'.")
            else:
                console.print("❌ Item not found.")

    def search_items_by_name(self, keyword: str) -> List[Item]:
        with get_db() as db:
            return db.query(Item).filter(Item.name.ilike(f"%{keyword}%")).all()

    def search_items_by_category_id(self, category_id: int):
        with get_db() as db:
            return db.query(Item).options(joinedload(Item.category)) \
                .filter(Item.category_id == category_id).all()

    def get_low_stock_items(self, threshold: int = 5) -> List[Item]:
        with get_db() as db:
            return db.query(Item).filter(Item.quantity < threshold).all()

