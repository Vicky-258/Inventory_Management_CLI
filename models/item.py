from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base import Base

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id', ondelete="SET NULL"), nullable=True)
    price = Column(Float, nullable=False)
    low_stock_threshold = Column(Integer, nullable=False, default=5)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    category = relationship("Categories", back_populates="items")
    supplier = relationship("Suppliers", back_populates="items")
    transactions = relationship("ItemTransactions", back_populates="item", cascade="all, delete-orphan")
