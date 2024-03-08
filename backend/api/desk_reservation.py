"""
    Reservation API

    This API is used to modify available resources.
"""

from fastapi import APIRouter, Depends, HTTPException
from ..models import User, Desk, DeskReservation
from ..services import DeskReservationService, UserPermissionError
from .authentication import registered_user

api = APIRouter(prefix="/api/reservation")

# List all desk reservations for admin.
@api.get("/admin/all", tags=['Reservation'])
def list_all_desk_reservations_for_admin(subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.list_all_desk_reservations_for_admin(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
# List future desk reservations for admin.
@api.get("/admin/future", tags=['Reservation'])
def list_future_desk_reservations_for_admin(subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.list_future_desk_reservations_for_admin(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

# List past desk reservations for admin.
@api.get("/admin/past", tags=['Reservation'])
def list_past_desk_reservations_for_admin(subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.list_past_desk_reservations_for_admin(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))    

# Remove desk reservation older than 1 month
@api.delete("/admin/remove_old", tags=['Reservation'])
def remove_old_desk_reservations(subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.remove_old_reservations(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

# List desk reservations by user
@api.get("/desk_reservations", tags=['Reservation'])
def list_desk_reservations_by_user(subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.list_desk_reservations_by_user(subject)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# List desk reservations by Desk ID
@api.get("/{desk_id}", tags=['Reservation'])
def list_desk_reservations_by_desk(desk_id: int, desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.list_reservations_by_desk(desk_id)
    except UserPermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# Reserve desk
@api.post("/reserve", tags=['Reservation'])
def create_desk_reservation(desk: Desk, reservation: DeskReservation, subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.create_desk_reservation(desk, subject, reservation)
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=422, detail=str(e))  


# Unreserve desk
@api.post("/unreserve", tags=['Reservation'])
def remove_desk_reservation(desk: Desk, reservation: DeskReservation, subject : User = Depends(registered_user), desk_res: DeskReservationService = Depends()):
    try:
        return desk_res.remove_desk_reservation(desk, subject, reservation)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    
