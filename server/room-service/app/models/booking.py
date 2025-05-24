# TO DO: Fahmi
from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed ="confirmed"
    cancelled = "cancelled"
    declined = "declined"

class Booking(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    start_time: datetime = Field(index=True)
    end_time: datetime = Field(index=True)
    status: BookingStatus = Field(default="pending", index=True)
