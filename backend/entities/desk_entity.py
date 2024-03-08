'''Desks that are able to be reserved.'''

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from .desk_reservation_entity import DeskReservationEntity
from ..models import Desk

class DeskEntity(EntityBase):
    __tablename__ = 'desk'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    desk_type: Mapped[str] = mapped_column(String(32), unique=False, index=True)
    included_resource: Mapped[str] = mapped_column(String(32), unique=False, index=True)
    available: Mapped[bool] = mapped_column(Boolean, default=True)

    desk_reservations: Mapped[list['DeskReservationEntity']] = relationship(back_populates='desk')

    @classmethod
    def from_model(cls, model: Desk) -> Self:
        return cls(
            id=model.id,
            tag=model.tag,
            desk_type=model.desk_type,
            included_resource=model.included_resource,
            available=model.available,
        )

    def to_model(self) -> Desk:
        return Desk(
            id=self.id,
            tag=self.tag,
            desk_type=self.desk_type,
            included_resource=self.included_resource,
            available=self.available,
        )

    def update(self, model: Desk) -> None:
        self.available = model.available