from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    declined = "declined"

class BookingCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    status: BookingStatus = BookingStatus.pending
