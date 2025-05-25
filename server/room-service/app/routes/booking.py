from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.models.booking import Booking, BookingCreate, BookingUpdate, BookingPublic
from app.models.room import Room
from app.services.db import get_session
from dateutil.parser import isoparse

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
async def read_booking(
    session: SessionDep, start: int = 1, end: Annotated[int, Query(le=100)] = 10
) -> list[BookingPublic]:
    return session.exec(select(Booking).offset(start - 1).limit(end - start + 1)).all()


@router.post("/", response_model=BookingPublic)
async def create_booking(booking: BookingCreate, session: SessionDep) -> BookingPublic:
    room = session.get(Room, booking.room_id)
    if not room:
        raise HTTPException(
            status_code=400, detail=f"Room with ID {booking.room_id} does not exist"
        )

    booking = Booking(
        room_id=booking.room_id,
        start_time=isoparse(str(booking.start_time)),
        end_time=isoparse(str(booking.end_time)),
        status=booking.status,
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


@router.get("/{booking_id}")
async def read_booking(booking_id: int, session: SessionDep) -> BookingPublic:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: int, booking_data: BookingUpdate, session: SessionDep) -> BookingPublic:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking_data_dict = booking_data.dict(exclude_unset=True)
    for key, value in booking_data_dict.items():
        setattr(booking, key, value)

    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, session: SessionDep):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(booking)
    session.commit()
    return {"ok": True, "message": f"Booking {booking_id} deleted successfully"}
