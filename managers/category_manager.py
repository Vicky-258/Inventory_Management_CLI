from db import get_db
from models import Category
from sqlalchemy.exc import SQLAlchemyError
from rich.console import Console

console = Console()

class CategoryManager:

    def add_category(self, name):
        with get_db() as session:
            try:
                exists = session.query(Category).filter_by(name=name.lower()).first()
                if exists:
                    console.print("❌ Category already exists.")
                else:
                    cat = Category(name=name.lower())
                    session.add(cat)
                    session.commit()
                    console.print(f"✅ Category '[bold green]{name}[/bold green]' added.")
            except SQLAlchemyError as e:
                session.rollback()
                console.print(f"❌ Error: {e}")

    def list_categories(self):
        with get_db() as session:
            return session.query(Category).all()

    def delete_category(self, name):
        with get_db() as session:
            try:
                category = session.query(Category).filter_by(name=name.lower()).first()
                if category:
                    session.delete(category)
                    session.commit()
                    console.print(f"🗑️ Category '[bold]{name}[/bold]' deleted.")
                else:
                    console.print("❌ Category not found.")
            except SQLAlchemyError as e:
                session.rollback()
                console.print(f"❌ Error: {e}")

    def get_category_by_name(self, name: str):
        with get_db() as db:
            return db.query(Category).filter(Category.name.ilike(name)).first()