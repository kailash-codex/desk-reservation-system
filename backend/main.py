"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from fastapi import FastAPI
from .api import desk_reservation, health, static_files, profile, authentication, user, desk
from .api.admin import users as admin_users
from .api.admin import roles as admin_roles

__authors__ = ["Kailash Muthu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

description = """
Welcome to the UNC Computer Science **Experience Labs** Application Programming Interface
"""

app = FastAPI(
    title="UNC CS Experience Labs API",
    version="0.0.1",
    description=description,
    openapi_tags=[health.openapi_tags],
)

app.include_router(user.api)
app.include_router(profile.api)
app.include_router(health.api)
app.include_router(authentication.api)
app.include_router(admin_users.api)
app.include_router(admin_roles.api)
app.include_router(desk_reservation.api)
app.include_router(desk.api)
app.mount("/", static_files.StaticFileMiddleware(directory="./static"))