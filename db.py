from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
