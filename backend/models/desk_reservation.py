"""Reservation model represents the date and time for a reservation created for a user."""

from pydantic import BaseModel
from datetime import datetime

class DeskReservation(BaseModel):
    id: int | None = None
    date: datetime | None = None