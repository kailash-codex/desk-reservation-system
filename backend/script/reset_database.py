"""Reset the database by dropping all tables, creating tables, and inserting demo data."""

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..database import engine
from ..env import getenv
from .. import entities

__authors__ = ["Kailash Muthu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


# Reset Tables
# entities.EntityBase.metadata.drop_all(engine)
# Reset Tables
# with engine.connect() as conn:
#     # Drop all tables with CASCADE
#     conn.execute(text(f'DROP TABLE IF EXISTS desk_desk_resource, desk_reservation, permission, user_role, role, user_entity, desk CASCADE'))

entities.EntityBase.metadata.drop_all(engine)

# Create Tables
entities.EntityBase.metadata.create_all(engine)

# Insert Dev Data from `script.dev_data`

# Add Users
with Session(engine) as session:
    from .dev_data import users
    to_entity = entities.UserEntity.from_model
    session.add_all([to_entity(model) for model in users.models])
    session.execute(text(f'ALTER SEQUENCE {entities.UserEntity.__table__}_id_seq RESTART WITH {len(users.models) + 1}'))
    session.commit()

# Add Roles
with Session(engine) as session:
    from .dev_data import roles
    to_entity = entities.RoleEntity.from_model
    session.add_all([to_entity(model) for model in roles.models])
    session.execute(text(f'ALTER SEQUENCE {entities.RoleEntity.__table__}_id_seq RESTART WITH {len(roles.models) + 1}'))
    session.commit()

# Add Users to Roles
with Session(engine) as session:
    from ..entities import UserEntity, RoleEntity
    from .dev_data import user_roles
    for user, role in user_roles.pairs:
        user_entity = session.get(UserEntity, user.id)
        role_entity = session.get(RoleEntity, role.id)
        user_entity.roles.append(role_entity)
    session.commit()

# Add Permissions to Users/Roles
with Session(engine) as session:
    from ..entities import PermissionEntity
    from .dev_data import permissions
    for role, permission in permissions.pairs:
        entity = PermissionEntity.from_model(permission)
        entity.role = session.get(RoleEntity, role.id)
        session.add(entity)
    session.execute(text(f'ALTER SEQUENCE permission_id_seq RESTART WITH {len(permissions.pairs) + 1}'))
    session.commit()

# Add Desks
with Session(engine) as session:
    from ..entities import DeskEntity
    from .dev_data import desks
    to_entity = entities.DeskEntity.from_model
    session.add_all([to_entity(model) for model in desks.models])
    session.execute(text(f'ALTER SEQUENCE {entities.DeskEntity.__table__}_id_seq RESTART WITH {len(desks.models) +1}'))
    session.commit()


# Add Reservations
with Session(engine) as session:
    from ..entities import DeskReservationEntity
    from .dev_data import desk_reservations
    
    for reservation, desk, user in desk_reservations.pairs:
        entity = DeskReservationEntity.from_model(reservation)
        entity.desk = session.get(DeskEntity, desk.id)
        entity.user = session.get(UserEntity, user.id)
        session.add(entity)
    session.execute(text(f'ALTER SEQUENCE {entities.DeskReservationEntity.__table__}_id_seq RESTART WITH {len(desk_reservations.models) + 1}'))
    session.commit()
