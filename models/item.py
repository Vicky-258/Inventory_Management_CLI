from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import ForeignKey
from db import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")
    added_on = Column(DateTime, default=datetime.now)
    transactions = relationship("Transaction", back_populates="item")

    def __repr__(self):
        return f"<Item(name='{self.name.title()}', qty={self.quantity}, price={self.price}, category={self.category})>"
