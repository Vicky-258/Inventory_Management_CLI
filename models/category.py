from sqlalchemy import Column, Integer, String
from db import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return self.name.title()

# 💬 SQL equivalent:
# CREATE TABLE categories (
#   id SERIAL PRIMARY KEY,
#   name VARCHAR UNIQUE NOT NULL
# );
