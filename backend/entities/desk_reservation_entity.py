from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from ..models import DeskReservation
from . import UserEntity
# from . import DeskEntity
from datetime import datetime

class DeskReservationEntity(EntityBase):
    __tablename__ = "desk_reservation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, unique=False)

    desk_id: Mapped[int] = mapped_column(ForeignKey('desk.id'), nullable=True)
    desk: Mapped['DeskEntity'] = relationship(back_populates='desk_reservations')

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    user: Mapped[UserEntity] = relationship(back_populates='desk_reservations')
    # __table_args__ = (UniqueConstraint('desk_id', 'date', name='reservation_detail'),UniqueConstraint('user_id', 'date', name='user_reservation_time'))

    @classmethod
    def from_model(cls, model: DeskReservation) -> Self:
        return cls(
            id=model.id,
            date=model.date,
        )
    
    def to_model(self) -> DeskReservation:
        print(self.date)
        return DeskReservation(
            id=self.id,
            date= self.date,
        )