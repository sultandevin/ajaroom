from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.models.booking import Booking
from app.schemas.booking import BookingCreate
from app.services.db import get_session

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def read_booking(
    session: SessionDep, start: int = 1, end: Annotated[int, Query(le=100)] = 10
) -> list[Booking]:
    return session.exec(select(Booking).offset(start - 1).limit(end - start + 1)).all()


@router.post("/", response_model=Booking)
def create_booking(data: BookingCreate, session: SessionDep) -> Booking:
    booking = Booking(
        start_time=data.start_time,
        end_time=data.end_time,
        status=data.status,
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking

@router.get("/{booking_id}")
def read_bookin(booking_id: int, session: SessionDep) -> Booking:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, session: SessionDep):
    hero = session.get(Booking, booking_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(hero)
    session.commit()
    return {"ok": True, "message": f"Booking {booking_id} deleted successfully"}
