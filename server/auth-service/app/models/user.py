from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    admin = Column(Boolean)
    hashed_password = Column(String)


class UserClass(BaseModel):
    username: str
    password: str
    email: str
    admin: bool = False

class RegUserClass(BaseModel):
    username: str
    password: str
    email: str