"""Sample reservation data. Subject to change as the reservation model changes."""

from ...models import DeskReservation
from datetime import datetime, timedelta
from . import desks, users

mar12_1200a1 = DeskReservation(id=1, date=datetime(2023, 4, 18, 9, 00))
mar12_1200a2 = DeskReservation(id=2, date=datetime(2023, 3, 19, 10, 00))
mar15_1350a2 = DeskReservation(id=3, date=datetime(2023, 3, 20, 11, 00))
thirty_one_days_ago = DeskReservation(id=4, date=datetime.now() - timedelta(days=31))
thirty_two_days_ago = DeskReservation(id=5, date=datetime.now() - timedelta(days=32))

models = [
    mar12_1200a1,
    mar12_1200a2,
    mar15_1350a2,
    thirty_one_days_ago,
    thirty_two_days_ago
]

pairs = [
    (mar12_1200a1, desks.a9, users.sol_student),
    (mar12_1200a2, desks.a10, users.sally_student),
    (mar15_1350a2, desks.a11, users.sol_student),
    (thirty_one_days_ago, desks.a9, users.sol_student),
    (thirty_two_days_ago, desks.a10, users.sol_student)
]