from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base import Base

class Suppliers(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now(UTC))

    items = relationship("Items", back_populates="supplier", passive_deletes=True)
