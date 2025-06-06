from typing import Annotated
from fastapi import APIRouter, HTTPException, Header, Depends, status
from sqlalchemy.orm import Session
from app.models.user import UserPublic
from app.service.db import getDB
from app.models.user import UserClass, RegUserClass, LoginRequest
from app.controllers.user import (
    get_user_by_name,
    get_user_by_email,
    create_user,
    create_user_by_admin,
    authenticate_user,
)
from app.controllers.jwt import oauth2_scheme
from app.controllers.jwt import create_access_token, verify_token

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    db: Annotated[Session, Depends(getDB)],
    user: UserClass | RegUserClass,
    Access_Token: str = Header(None),
):
    if get_user_by_name(db, user.username) or get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
        )
    if Access_Token is not None:
        try:
            payload = verify_token(Access_Token)
            if payload["admin"]:
                return create_user_by_admin(db, user)
        except:
            pass
    return create_user(db, user)


@router.post("/token")
def login_for_acc_token(
    db: Annotated[Session, Depends(getDB)],
    form_data: LoginRequest,
):
    user = authenticate_user(db, form_data.usernameormail, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "admin": user.admin}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token")
async def verify_user_token(Access_Token: str = Header(...)):
    if not Access_Token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No token provided"
        )
    return verify_token(Access_Token)


@router.get("/me", response_model=UserPublic)
async def get_current_user(
    db: Annotated[Session, Depends(getDB)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except HTTPException as e:  # Catch exceptions from verify_token if it raises them
        raise e
    except Exception:  # Catch any other unexpected errors during token verification
        raise credentials_exception

    user = get_user_by_name(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
