from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.services.db import create_db_and_tables
from app.routes import room, booking

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(room.router, prefix="/rooms", tags=["rooms"])
app.include_router(booking.router, prefix="/bookings", tags=["bookings"])


@app.get("/")
def root():
    return {
        "message": "Welcome to the Room Service API",
    }
