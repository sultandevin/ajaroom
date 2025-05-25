from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.service.db import getDB
from app.models.user import RegUserClass
from app.controllers.user import get_user_by_name, get_user_by_email, create_user, authenticate_user
from app.controllers.jwt import create_access_token, verify_token

router = APIRouter()

@router.post("/register")
def register_user(db: Annotated[Session, Depends(getDB)], user: RegUserClass):
    if get_user_by_name(db, user.username) or get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
    return create_user(db, user)

@router.post("/token")
def login_for_acc_token(db: Annotated[Session, Depends(getDB)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.username, "id": user.id, "admin": user.admin})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token)
    return {"message": "Valid token"}
    