from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

Database_URL = "postgresql://postgres:newpassword@localhost:5432/new_todo"

engine = create_engine(Database_URL)

SessionLocal = sessionmaker(autocommit = False , autoflush=False , bind = engine)

Base = declarative_base()

def get_db ():
    db = SessionLocal()
    try:
        yield db 
    finally :
        db.close()
