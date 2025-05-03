from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from enum import Enum
from .base import Base

class TransactionType(Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"

class ItemTransactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    transaction_type = Column(SQLEnum(TransactionType, name="transaction_type_enum"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    item = relationship("Items", back_populates="transactions")
