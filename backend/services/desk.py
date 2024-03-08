from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import User, Desk
from ..entities import DeskEntity, DeskReservationEntity
from .permission import PermissionService
from datetime import datetime

class DeskService:
    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission
    

    def list_all_desks(self, subject: User) -> list[Desk]:
        """List all desks.

        Args:
            subject: The user performing the action.

        Returns:
            list[Desk]: A list of all desk entities.
        
        Raises:
            PermissionError: If the subject does not have permission to admin access.
        """
        self._permission.enforce(subject, 'admin/', 'desk')
        stmt = select(DeskEntity).order_by(DeskEntity.id)
        desk_entities = self._session.execute(stmt).scalars()
        return [desk_entity.to_model() for desk_entity in desk_entities]
    

    def list_available_desks(self) -> list[Desk]:
        """List available desks.

        Returns:
            list[Desk]: A list of available desk entities.
        """
        stmt = select(DeskEntity).where(DeskEntity.available == True).order_by(DeskEntity.id)
        desk_entities = self._session.execute(stmt).scalars()
        return [desk_entity.to_model() for desk_entity in desk_entities]
    

    def create_desk(self, desk: Desk, subject: User) -> Desk:
        """Create a new desk.

        Args:
            desk: The desk to create.

        Returns:
            Desk: The created desk entity.
        
        Raises:
            PermissionError: If the subject does not have permission to admin access.
        """
        self._permission.enforce(subject, 'admin/', 'desk')
        desk_entity = DeskEntity.from_model(desk)
        self._session.add(desk_entity)
        self._session.commit()
        return desk_entity.to_model()


    def remove_desk(self, desk: Desk, subject: User) -> Desk:
        """Remove a desk.

        Args:
            desk: The desk to remove.

        Returns:
            Desk: The removed desk entity.

        Raises:
            PermissionError: If the subject does not have permission to admin access.
        """
        self._permission.enforce(subject, 'admin/', 'desk')
        desk_entity = self._session.get(DeskEntity, desk.id)
        self._session.delete(desk_entity)
        self._session.commit()
        return desk_entity.to_model()
    
    
    def toggle_desk_availability(self, desk: Desk, subject: User) -> Desk:
        """Toggles whether a desk is able to be reserved and removes any reservations for the desk if it is made unavailable.
        Args:
            desk: The desk to toggle.
        Returns:
            Desk: The updated desk entity.
        """
        self._permission.enforce(subject, 'admin/', 'desk')
        desk_entity = self._session.get(DeskEntity, desk.id)
        if desk_entity.available:
            desk_entity.available = False
        else:
            desk_entity.available = True
        if not desk_entity.available:
            stmt = delete(DeskReservationEntity)\
                .where(DeskReservationEntity.desk_id == desk.id) \
                .where(DeskReservationEntity.date >= datetime.now().replace(minute=0, second=0, microsecond=0))
            self._session.execute(stmt)
        self._session.commit()
        return desk_entity.to_model()
    

    def get_desk_by_id(self, desk_id: int) -> Desk:
        """Get a desk by its ID.

        Args:
            desk_id: The ID of the desk to retrieve.

        Returns:
            Desk: The desk entity with the specified ID.
        """
        stmt = select(DeskEntity).where(DeskEntity.id == desk_id)
        desk_entity = self._session.execute(stmt).scalar_one_or_none()
        return desk_entity.to_model()
    
    
    def update_desk(self, desk_id: int, desk: Desk, subject: User) -> Desk:
        """Update an existing desk.

        Args:
            desk_id: The id of the desk to update.
            desk: The updated desk information.
            subject: The user performing the action.

        Returns:
            Desk: The updated desk entity.
        """
        self._permission.enforce(subject, 'admin/', 'desk')
        desk_entity = self._session.get(DeskEntity, desk_id)
        desk_entity.desk_type = desk.desk_type
        desk_entity.included_resource = desk.included_resource
        desk_entity.available = desk.available
        self._session.commit()
        return desk_entity.to_model()