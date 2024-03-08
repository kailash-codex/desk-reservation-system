""" 
    Desk API:
        This API is only for calling desks.

"""

from fastapi import APIRouter, Depends, HTTPException
from ..models import User, Desk
from ..services import UserPermissionError, DeskService
from .authentication import registered_user

api = APIRouter(prefix="/api/desk")

# List all desks in the database.
@api.get("", tags=['Desk'])
def list_all_desks(subject : User = Depends(registered_user), desk_service: DeskService = Depends()):
    try:
        return desk_service.list_all_desks(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    

# List available desks
@api.get("/available", tags=['Desk'])
def list_available_desks(desk_service: DeskService = Depends()):
    try:
        return desk_service.list_available_desks()
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    

# Create Desk (For admin)
@api.post("/admin/create_desk", tags=['Desk'])
def create_desk(desk: Desk, subject : User = Depends(registered_user), desk_service: DeskService = Depends()):
    try:
        return desk_service.create_desk(desk, subject)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    

# Remove Desk (For admin)
@api.post("/admin/remove_desk", tags=['Desk'])
def remove_desk(desk: Desk, subject : User = Depends(registered_user), desk_service: DeskService = Depends()):
    try:
        return desk_service.remove_desk(desk, subject)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    
# Toggle Desk Availability (For admin)
@api.put("/admin/toggle_availability", tags=['Desk'])
def toggle_desk_availability(desk: Desk, subject : User = Depends(registered_user), desk_service: DeskService = Depends()):
    try:
        return desk_service.toggle_desk_availability(desk, subject)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    

# Get Desk by Desk ID
@api.get("/{desk_id}", tags=['Desk'])
def get_desk_desk_id(desk_id: int, desk_service: DeskService = Depends()):
    try:
        return desk_service.get_desk_by_id(desk_id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


# Update Desk
@api.put("/admin/update_desk/{desk_id}", tags=['Desk'])
def update_desk(desk_id: int, desk: Desk, subject : User = Depends(registered_user), desk_service: DeskService = Depends()):
    try:
        return desk_service.update_desk(desk_id, desk, subject)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))