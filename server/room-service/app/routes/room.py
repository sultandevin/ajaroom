from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.models.room import RoomCreate, RoomPublic, Room
from app.services.db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
async def read_rooms(
    session: SessionDep, start: int = 1, end: Annotated[int, Query(le=100)] = 10
) -> list[RoomPublic]:
    return session.exec(select(Room).offset(start - 1).limit(end - start + 1)).all()


@router.post("/")
async def create_room(room: RoomCreate, session: SessionDep) -> RoomPublic:
    room = Room.from_orm(room)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


@router.get("/{room_id}")
async def read_room(room_id: int, session: SessionDep) -> RoomPublic:
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.delete("/{room_id}")
async def delete_room(room_id: int, session: SessionDep):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    session.delete(room)
    session.commit()
    return {"ok": True, "message": f"Room {room_id} deleted successfully"}
