from sqlmodel import Field, SQLModel


class Room(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)  # required
    location: str = Field(index=True, max_length=200)  # required
    capacity: int = Field(index=True)  # required
    description: str | None = Field(default=None, max_length=500)
    available: bool = Field(default=True)
