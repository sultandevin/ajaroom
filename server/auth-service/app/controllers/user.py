import os
from sqlalchemy.orm import Session
from app.models.user import User, UserClass, RegUserClass
from passlib.context import CryptContext

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: RegUserClass):
    new_user=User(
        username=user.username,
        email=user.email,
        admin=False, 
        hashed_password=hash_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return "User created successfully"

def create_user_by_admin(db: Session, user: UserClass | RegUserClass):
    new_user=User(
        username=user.username,
        email=user.email,
        admin=user.admin if user.admin else False, 
        hashed_password=hash_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return "User created successfully"

def authenticate_user(db: Session, input_cred: str, password: str):
    user = get_user_by_name(db, input_cred)
    if not user:
        user = get_user_by_email(db, input_cred)
        if not user:
            return False
    if not hash_context.verify(password, user.hashed_password):
        return False
    return user