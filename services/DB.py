from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Items, Categories, Suppliers, ItemTransactions

DATABASE_URL = 'sqlite:///DataBase.db'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)

def get_session():
    return Session()