from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    action = Column(String, nullable=False)  # 'buy' or 'sell'
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="transactions")
    item = relationship("Item", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction({self.action} {self.quantity} of {self.item.name} by {self.user.username})>"
