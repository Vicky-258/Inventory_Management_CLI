from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum
from datetime import datetime, UTC

Base = declarative_base()

class TransactionType(Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    item = relationship("Items", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, item_id={self.item_id}, quantity={self.quantity}, type={self.transaction_type}, timestamp={self.timestamp})>"




class Items(Base):
    __tablename__ = 'items'  # Consistent lowercase table names

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)  # Unique index for faster lookups
    description = Column(Text)  # Use Text instead of String for long descriptions
    category_id = Column(Integer, ForeignKey('Categories.id', ondelete="CASCADE"), nullable=False)
    supplier_id = Column(Integer, ForeignKey('Suppliers.id', ondelete="SET NULL"), nullable=True)
    price = Column(Float, nullable=False)
    low_stock_threshold = Column(Integer, nullable=False, default=5)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))  # UTC for consistency
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    # Relationships (Allows us to access `item.category.name` and `item.supplier.name`)
    category = relationship("Categories", back_populates="items")
    supplier = relationship("Suppliers", back_populates="items")

    def __repr__(self):
        return f"<Item(name={self.name}, price={self.price}, quantity={self.quantity}, category_id={self.category_id}, supplier_id={self.supplier_id})>"


class Categories(Base):
    __tablename__ = 'categories'  # Standard lowercase table naming

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)  # Unique & indexed for faster search
    created_at = Column(DateTime, default=datetime.now(UTC))  # Optional: Logs when category was added

    # Relationship with Items
    items = relationship("Items", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"


class Suppliers(Base):
    __tablename__ = 'suppliers'  # Consistent lowercase table naming

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)  # Unique supplier names
    email = Column(String, nullable=False, unique=True, index=True)  # Unique & indexed for faster searches
    phone = Column(String, nullable=False, unique=True)  # Prevent duplicate phone numbers
    created_at = Column(DateTime, default=datetime.now(UTC))  # Timestamp for tracking

    # Relationship with Items
    items = relationship("Items", back_populates="supplier", passive_deletes=True)

    def __repr__(self):
        return f"<Supplier(id={self.id}, name={self.name}, email={self.email}, phone={self.phone})>"