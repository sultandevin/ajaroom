from sqlmodel import Session
from app.services.db import (
    create_db_and_tables,
    engine,
    sqlite_file_name,
)
from app.models.room import Room
from app.models.booking import Booking
from datetime import datetime
import os  # Added import


def seed_data():
    # Remove the old database file if it exists
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)
        print(f"Removed old database file: {sqlite_file_name}")
    else:
        print(f"Database file {sqlite_file_name} not found, will create a new one.")

    create_db_and_tables()

    with Session(engine) as session:
        # seed rooms
        rooms = [
            Room(
                name="Basecamp Himakom",
                location="Toilet Lantai 5",
                description="A cozy place for meetings.",
                capacity=6,
            ),
            Room(
                name="Basecamp OmahTI",
                location="WISMA FMIPA UGM G-13",
                description="Tempat terbaik untuk semua hal.",
                capacity=20,
            ),
        ]
        session.add_all(rooms)

        # seed bookings
        bookings = [
            Booking(
                room_id=1,
                start_time=datetime.fromisoformat("2025-06-01T09:00"),
                end_time=datetime.fromisoformat("2025-06-01T11:00"),
            ),
            Booking(
                room_id=2,
                start_time=datetime.fromisoformat("2025-06-01T10:00"),
                end_time=datetime.fromisoformat("2025-06-01T12:00"),
            ),
        ]
        session.add_all(bookings)

        session.commit()
        print("✅ Seeded dummy data successfully!")


if __name__ == "__main__":
    seed_data()
    print("Seeding complete.")
