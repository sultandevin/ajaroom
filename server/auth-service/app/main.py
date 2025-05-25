import os
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.routes import user
from app.service.db import create_table


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_table()


load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(user.router, prefix="/auth", tags=["auth"])


@app.get("/")
def root():
    return {"message": "Auth Service is running."}


@app.get("/login")
def login():
    return {"message": "Successfully logged in!"}
