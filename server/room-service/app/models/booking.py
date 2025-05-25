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
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    start_time: datetime = Field(index=True)
    end_time: datetime = Field(index=True)
    status: BookingStatus = Field(default="pending", index=True)


# Model representing a booking in the database
class Booking(BookingBase, table=True):
    id: int = Field(default=None, primary_key=True)


# Payload for creating a booking
class BookingCreate(BookingBase):
    pass

# Payload for updating a booking
class BookingUpdate(SQLModel):
    room_id: Optional[int] = Field(default=None, foreign_key="room.id")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatus] = None

# Representation of a booking for public API responses
class BookingPublic(BookingBase):
    id: int
