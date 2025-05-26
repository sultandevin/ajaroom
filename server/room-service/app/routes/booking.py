from typing import Annotated, Dict
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from app.models.booking import Booking, BookingCreate, BookingUpdate, BookingPublic
from app.models.room import Room
from app.services.db import get_session
from app.controllers.auth import ensure_authenticated, oauth2_scheme
from dateutil.parser import isoparse
import os
import httpx

router = APIRouter(dependencies=[Depends(ensure_authenticated)])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
async def read_booking(
    session: SessionDep, start: int = 1, end: Annotated[int, Query(le=100)] = 10
) -> list[BookingPublic]:
    return session.exec(select(Booking).offset(start - 1).limit(end - start + 1)).all()


@router.post("/", response_model=BookingPublic)
async def create_booking(
    booking: Booking,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> BookingPublic:
    room = session.get(Room, booking.room_id)
    if not room:
        raise HTTPException(
            status_code=400, detail=f"Room with ID {booking.room_id} does not exist"
        )

    start_time = isoparse(str(booking.start_time))
    end_time = isoparse(str(booking.end_time))

    if start_time >= end_time:
        raise HTTPException(
            status_code=400, detail="Start time must be earlier than end time."
        )

    if booking.status == "confirmed":
        conflict_stmt = select(Booking).where(
            Booking.room_id == booking.room_id,
            Booking.status == "confirmed",
            Booking.end_time > start_time,
            Booking.start_time < end_time,
        )
        conflict = session.exec(conflict_stmt).first()
        if conflict:
            raise HTTPException(
                status_code=409,
                detail=f"Conflict with existing confirmed booking (ID: {conflict.id})",
            )

    # Get user information from user service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{os.getenv('AUTH_SERVICE_URL', 'http://auth-service:5000')}/me",
                headers={"Authorization": f"Bearer {token}"},
            )
            print(response)
            response.raise_for_status()
            user_data = response.json()
            user_email = user_data.get("email")
            if not user_email:
                raise HTTPException(
                    status_code=400,
                    detail="User email not found in user service response",
                )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Error contacting user service: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"User service error: {str(e)}",
            )

    booking_to_save = Booking(
        user_email=user_email,
        room_id=booking.room_id,
        start_time=start_time,
        end_time=end_time,
        status=booking.status,
    )
    session.add(booking_to_save)
    session.commit()
    session.refresh(booking_to_save)
    return booking_to_save


@router.get("/{booking_id}")
async def read_booking(booking_id: int, session: SessionDep) -> BookingPublic:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=BookingPublic)
async def update_booking(
    booking_id: int, booking_data: BookingUpdate, session: SessionDep
) -> BookingPublic:
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    start_time = isoparse(str(booking.start_time))
    end_time = isoparse(str(booking.end_time))
    status = booking_data.status

    if start_time >= end_time:
        raise HTTPException(
            status_code=400, detail="Start time must be earlier than end time."
        )

    if status == "confirmed":
        conflict_stmt = select(Booking).where(
            Booking.room_id == booking.room_id,
            Booking.id != booking_id,
            Booking.status == "confirmed",
            Booking.end_time > start_time,
            Booking.start_time < end_time,
        )
        conflict = session.exec(conflict_stmt).first()
        if conflict:
            raise HTTPException(
                status_code=409,
                detail=f"Conflict with confirmed booking ID {conflict.id} in same time slot.",
            )

    booking.status = booking_data.status

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
