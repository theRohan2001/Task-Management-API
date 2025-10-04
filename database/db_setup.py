from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()