"""Package for all models in the application."""

from .pagination import Paginated, PaginationParams
from .permission import Permission
from .user import User, ProfileForm, NewUser
from .role import Role
from .role_details import RoleDetails
from .desk import Desk
from .desk_reservation import DeskReservation

__authors__ = ["Kailash Muthu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"
