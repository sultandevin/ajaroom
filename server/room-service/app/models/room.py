from sqlmodel import Field, SQLModel
from typing import Optional


class RoomBase(SQLModel):  # Create a base model for common fields
    name: str = Field(index=True, max_length=100)
    location: str = Field(index=True, max_length=200)
    capacity: int = Field(index=True)
    description: Optional[str] = Field(default=None, max_length=500, nullable=True)
    available: bool = Field(default=True)


# Model representing a room in the database
class Room(RoomBase, table=True):
    id: int = Field(default=None, primary_key=True)


# Payload for creating a room
class RoomCreate(RoomBase):
    pass

# Representation of a room for public API responses
class RoomPublic(RoomBase):
    id: int
