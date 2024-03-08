"""Desk model serves as the data object for representing desks that can be reserved"""

from pydantic import BaseModel

class Desk(BaseModel):
    id: int | None = None
    tag: str = ""
    desk_type: str = ""
    included_resource: str = ""
    available: bool = True

