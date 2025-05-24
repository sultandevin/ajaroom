from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.models.room import Room
from app.services.db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def read_rooms(
    session: SessionDep, start: int = 1, end: Annotated[int, Query(le=100)] = 10
) -> list[Room]:
    return session.exec(select(Room).offset(start - 1).limit(end - start + 1)).all()


@router.post("/")
def create_room(room: Room, session: SessionDep) -> Room:
    session.add(room)
    session.commit()
    session.refresh(room)
    return room


@router.get("/{room_id}")
def read_room(room_id: int, session: SessionDep) -> Room:
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.delete("/{room_id}")
def delete_room(room_id: int, session: SessionDep):
    hero = session.get(Room, room_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Room not found")
    session.delete(hero)
    session.commit()
    return {"ok": True, "message": f"Room {room_id} deleted successfully"}
