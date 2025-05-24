from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User

SQLALCHEMY_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})

session = sessionmaker(engine)

def create_table():
    User.metadata.create_all(bind=engine)

def getDB():
    db = session()
    try:
        yield db
    finally:
        db.close()