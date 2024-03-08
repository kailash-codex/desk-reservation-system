from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Desk, DeskReservation
from ..entities import UserEntity, DeskEntity, DeskReservationEntity
from .permission import PermissionService
from datetime import datetime, timedelta

class DeskReservationService:
    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission
    

    def list_future_desk_reservations_for_admin(self, subject: User) -> list[(DeskReservation, Desk, User)]:
        """List all desk reservations for admin.

        Args:
            subject: The user performing the action.

        Returns:
            list[(DeskReservation, Desk, User)]: A list of tuples, each containing a desk reservation entity, its associated desk entity, and the user who reserved the desk.
        
        Raises:
            PermissionError: If the subject does not have permission to admin access.
        """
        self._permission.enforce(subject, 'admin/', 'desk_reservation')
        stmt = select(DeskReservationEntity, DeskEntity, UserEntity)\
            .join(DeskEntity)\
            .join(UserEntity)\
            .where(DeskReservationEntity.date >= datetime.now().replace(minute=0, second=0, microsecond=0)) \
            .order_by(DeskReservationEntity.date)
        reservation_entities = self._session.execute(stmt).all()
        return [(desk_reservation_entity, desk_entity, user_entity) for desk_reservation_entity, desk_entity, user_entity in reservation_entities]
    

    def list_past_desk_reservations_for_admin(self, subject: User) -> list[(DeskReservation, Desk, User)]:
        """List all desk reservations for admin.

        Args:
            subject: The user performing the action.

        Returns:
            list[(DeskReservation, Desk, User)]: A list of tuples, each containing a desk reservation entity, its associated desk entity, and the user who reserved the desk.
        
        Raises:
            PermissionError: If the subject does not have permission to admin access.
        """
        self._permission.enforce(subject, 'admin/', 'desk_reservation')
        stmt = select(DeskReservationEntity, DeskEntity, UserEntity)\
            .join(DeskEntity)\
            .join(UserEntity)\
            .where(DeskReservationEntity.date < datetime.now().replace(minute=0, second=0, microsecond=0)) \
            .order_by(DeskReservationEntity.date)
        reservation_entities = self._session.execute(stmt).all()
        return [(desk_reservation_entity, desk_entity, user_entity) for desk_reservation_entity, desk_entity, user_entity in reservation_entities]
    

    def remove_old_reservations(self, subject: User) -> int:
        """Remove desk reservations older than 1 month.
        
        Args:
            subject: The user performing the action.
        Returns:
            None
        Raises:
            PermissionError: If the subject does not have permission to admin access.
        """
        self._permission.enforce(subject, 'admin/', 'desk_reservation')
        stmt = delete(DeskReservationEntity)\
            .where(DeskReservationEntity.date < (datetime.now() - timedelta(days=30)))
        self._session.execute(stmt)
        self._session.commit()
        return 204


    def list_desk_reservations_by_user(self, user: User) -> list[(DeskReservation, Desk)]:
        """List desk reservations by user.

        Args:
            user: The user whose reservations to retrieve.

        Returns:
            list[(DeskReservation, Desk)]: A list of tuples, each containing a desk reservation entity and its associated desk entity from from the current date onwards.
        """
        stmt = select(DeskReservationEntity, DeskEntity)\
            .join(DeskEntity)\
            .where(DeskReservationEntity.user_id == user.id)\
            .where(DeskReservationEntity.date >= datetime.now().replace(minute=0, second=0, microsecond=0)) \
            .order_by(DeskReservationEntity.date)
        reservation_entities = self._session.execute(stmt).all()
        return [(desk_reservation_entity, desk_entity) for desk_reservation_entity, desk_entity in reservation_entities]
    

    def list_reservations_by_desk(self, desk_id: int) -> list[DeskReservation]:
        """List reservations by desk.
        
        Args:
            desk_id: The ID of the desk whose reservations to retrieve.
            
        Returns:
            list[DeskReservation]: A list of desk reservation entities.
        """

        stmt = select(DeskReservationEntity)\
            .where(DeskReservationEntity.desk_id == desk_id) \
            .where(DeskReservationEntity.date >= datetime.now().replace(minute=0, second=0, microsecond=0))
        reservations = self._session.execute(stmt).scalars()
        return [reservation.to_model() for reservation in reservations]


    def create_desk_reservation(self, desk: Desk, user: User, reservation: DeskReservation) -> DeskReservation:
        """Create a desk reservation.

        Args:
            desk: The desk to reserve.
            user: The user reserving the desk.
            reservation: The desk reservation details.

        Returns:
            DeskReservation: The created desk reservation entity.
        """

        reservation_entity = DeskReservationEntity.from_model(reservation)
        reservation_entity.user_id = user.id
        reservation_entity.desk_id = desk.id
        self._session.add(reservation_entity)
        self._session.commit()
        return reservation_entity.to_model()


    def remove_desk_reservation(self, desk: Desk, user: User, reservation: DeskReservation) -> Desk:
        """Remove a desk reservation.

        Args:
            desk: The desk whose reservation to remove.
            user: The user who reserved the desk.
            reservation: The reservation to remove.

        Returns:
            Desk: The updated desk entity.
        """
        
        reservation_entity = self._session.get(DeskReservationEntity, reservation.id)
        reservation_entity.user_id = user.id
        reservation_entity.desk_id = desk.id
        self._session.delete(reservation_entity)
        self._session.commit()
        return reservation_entity.to_model()
      
    
    
    