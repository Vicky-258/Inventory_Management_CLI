from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from db import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    category = Column(String, default="Uncategorized")  # 👈 NEW
    added_on = Column(DateTime, default=datetime.now)


    def __repr__(self):
        return f"<Item(name='{self.name}', qty={self.quantity}, price={self.price}, category={self.category})>"
