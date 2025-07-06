from sqlalchemy import Column, Integer, String
from db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}')>"
