from sqlmodel import Field, SQLModel


class Room(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    capacity: int = Field(index=True)
    available: bool = Field(default=True)
