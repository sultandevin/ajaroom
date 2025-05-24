from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.models.booking import Booking
from app.services.db import get_session
from dateutil.parser import isoparse

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
async def read_booking(
    session: SessionDep, start: int = 1, end: Annotated[int, Query(le=100)] = 10
) -> list[Booking]:
    return session.exec(select(Booking).offset(start - 1).limit(end - start + 1)).all()


@router.post("/", response_model=Booking)
async def create_booking(booking: Booking, session: SessionDep) -> Booking:
    booking = Booking(
        start_time=isoparse(str(booking.start_time)),
        end_time=isoparse(str(booking.end_time)),
        status=booking.status,
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


@router.get("/{booking_id}")
async def read_booking(booking_id: int, session: SessionDep) -> Booking:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, session: SessionDep):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(booking)
    session.commit()
    return {"ok": True, "message": f"Booking {booking_id} deleted successfully"}
