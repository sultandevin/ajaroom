from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum
from typing import Optional


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    declined = "declined"


class BookingBase(SQLModel):
    pass


# Model representing a booking in the database
class Booking(BookingBase, table=True):
    id: int = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    start_time: datetime = Field(index=True)
    end_time: datetime = Field(index=True)
    user_email: str = Field(index=True, nullable=False)
    status: BookingStatus = Field(default="pending", index=True)


# Payload for creating a booking
class BookingCreate(BookingBase):
    room_id: int
    start_time: datetime
    end_time: datetime
    user_email: str
    status: BookingStatus


# Payload for updating a booking
class BookingUpdate(BookingBase):
    status: Optional[BookingStatus] = None


# Representation of a booking for public API responses
class BookingPublic(BookingBase):
    id: int
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    start_time: datetime = Field(index=True)
    end_time: datetime = Field(index=True)
    user_email: str
    status: BookingStatus
