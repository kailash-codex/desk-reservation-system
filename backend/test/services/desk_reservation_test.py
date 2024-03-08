import pytest

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ...models import User, Desk, DeskReservation, Role
from ...entities import UserEntity, DeskEntity, PermissionEntity, RoleEntity
from ...services import DeskReservationService, PermissionService, UserPermissionError

# Mock Models #
# Desks
desk1 = Desk(id=1, tag='AA1', desk_type='Computer Desk', included_resource='Pro Display XDR w/ Mac Pro', available=True)
desk2 = Desk(id=2, tag='CD1', desk_type='Standing Desk', included_resource='Windows Desktop i9', available=True)
desk3 = Desk(id=3, tag='ND1', desk_type='Standing Desk', included_resource='iMac w/ Pro Display', available=True)


# Root User
root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu')
root_role = Role(id=1, name='root')

# Student User
student1 = User(id=2, pid=123456789, onyen='student1', email='student1@unc.edu')
student2 = User(id=3, pid=987654321, onyen='student2', email='student2@unc.edu')
student3 = User(id=4, pid=123456780, onyen='student3', email='student3@unc.edu')


# Desk Reservations
reservation1 = DeskReservation(id=1, date=datetime.now() + timedelta(days=1))
reservation2 = DeskReservation(id=2, date=datetime.now() + timedelta(days=2))
reservation3 = DeskReservation(id=3, date=datetime.now() + timedelta(days=3))
reservation4 = DeskReservation(id=4, date=datetime.now() - timedelta(days=1))
reservation5 = DeskReservation(id=5, date=datetime.now() - timedelta(days=2))

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    
    # Bootstrap for root User and Role
    root_user_entity = UserEntity.from_model(root)
    test_session.add(root_user_entity)
    root_role_entity = RoleEntity.from_model(root_role)
    root_role_entity.users.append(root_user_entity)
    test_session.add(root_role_entity)
    root_permission_entity = PermissionEntity(
        action='*', resource='*', role=root_role_entity)
    test_session.add(root_permission_entity)

    # Bootstrap for Desks
    desk1_entity = DeskEntity.from_model(desk1)
    desk2_entity = DeskEntity.from_model(desk2)
    desk3_entity = DeskEntity.from_model(desk3)

    test_session.add(desk1_entity)
    test_session.add(desk2_entity)
    test_session.add(desk3_entity)

    test_session.commit()

    # Bootstrap for Student User
    student1_entity = UserEntity.from_model(student1)
    student2_entity = UserEntity.from_model(student2)
    student3_entity = UserEntity.from_model(student3)

    test_session.add(student1_entity)
    test_session.add(student2_entity)
    test_session.add(student3_entity)

    test_session.commit()

    yield

# pytest fixture to use for all the tests.
@pytest.fixture()
def desk_reservation_service(test_session: Session):
    return DeskReservationService(test_session)

# Test listing future desk reservations (for Admin).
def test_list_future_desk_reservations_for_admin(test_session: Session):
    permission = PermissionService(test_session)
    desk_reservation_service = DeskReservationService(test_session, permission)
    desk_reservation_service._permission.enforce(root, 'admin/', '*')

    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation2)
    desk_reservation_service.create_desk_reservation(desk3, student3, reservation3)
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation4)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation5)

    future_reservations = desk_reservation_service.list_future_desk_reservations_for_admin(root)

    assert future_reservations is not None
    assert len(future_reservations) == 3

# Test listing past desk reservations (for Admin).
def test_list_past_desk_reservations_for_admin(test_session: Session):
    permission = PermissionService(test_session)
    desk_reservation_service = DeskReservationService(test_session, permission)
    desk_reservation_service._permission.enforce(root, 'admin/', '*')

    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation2)
    desk_reservation_service.create_desk_reservation(desk3, student3, reservation3)
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation4)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation5)

    past_reservations = desk_reservation_service.list_past_desk_reservations_for_admin(root)

    assert past_reservations is not None
    assert len(past_reservations) == 2

# Test the removal of old reservations (for Admin).
def test_remove_old_reservations(test_session: Session):
    permission = PermissionService(test_session)
    desk_reservation_service = DeskReservationService(test_session, permission)
    desk_reservation_service._permission.enforce(root, 'admin/', '*')

    reservation6 = DeskReservation(id=6, date=datetime.now() - timedelta(days=31))
    
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation2)
    desk_reservation_service.create_desk_reservation(desk3, student3, reservation3)
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation4)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation5)
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation6)

    desk_reservation_service.remove_old_reservations(root)
    reservation = desk_reservation_service.list_past_desk_reservations_for_admin(root)
    assert len(reservation) == 2

# Test listing all desk reservations (Testing for student)
def test_list_desk_reservations_as_student(test_session: Session):
    permission = PermissionService(test_session)
    desk_reservation_service = DeskReservationService(test_session, permission)

    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation2)

    with pytest.raises(UserPermissionError):
        desk_reservation_service.list_future_desk_reservations_for_admin(student1)
        desk_reservation_service.list_past_desk_reservations_for_admin(student1)
    

# Test desk reservation by user.
def test_list_desk_reservations_by_user(desk_reservation_service: DeskReservationService):
    
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk2, student1, reservation2)
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation3)

    list_reservation_by_user = desk_reservation_service.list_desk_reservations_by_user(student1)
    assert len(list_reservation_by_user) == 3
    assert [reservation[1].tag for reservation in list_reservation_by_user if reservation[1].tag == 'CD1'] 


# Test to create reservation of desk.
def test_create_reservation(desk_reservation_service: DeskReservationService):

    desk4 = Desk(id=1, tag='AA1', desk_type='Computer Desk', included_resource='Pro Display XDR w/ Mac Pro', available=True)
    reservation4 = DeskReservation(id=3, date=datetime.now() + timedelta(days=4))
    new_desk_reservation = desk_reservation_service.create_desk_reservation(desk4, student3, reservation4)

    with pytest.raises(IntegrityError):
        desk_reservation_service.create_desk_reservation(desk4, student3, reservation4)
    
    assert new_desk_reservation.date == reservation4.date
    assert new_desk_reservation is not None
    

# Test to remove the desk reservation.
def test_remove_desk_reservation(desk_reservation_service: DeskReservationService):
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)

    remove_reservation = desk_reservation_service.remove_desk_reservation(desk1, student1, reservation1)
    assert remove_reservation.date == reservation1.date
    assert remove_reservation.id == desk1.id


# Test to list the desk reservations by desk.
def test_list_desk_reservations_by_desk(desk_reservation_service: DeskReservationService):
    
    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk1, student2, reservation2)
    desk_reservation_service.create_desk_reservation(desk1, student3, reservation3)

    desk_reservations = desk_reservation_service.list_reservations_by_desk(desk1.id)
    
    assert len(desk_reservations) == 3
    assert desk_reservations == [reservation1, reservation2, reservation3]
    assert desk_reservations[0].id == 1
    assert desk_reservations[1].date == reservation2.date


# Test that listing desk reservations only returns the reservations for that desk.
def test_reservation_by_desk_multiple_desk(desk_reservation_service: DeskReservationService):

    desk_reservation_service.create_desk_reservation(desk1, student1, reservation1)
    desk_reservation_service.create_desk_reservation(desk1, student2, reservation2)
    desk_reservation_service.create_desk_reservation(desk3, student3, reservation3)

    
    desk_reservations = desk_reservation_service.list_reservations_by_desk(desk1.id)

    assert len(desk_reservations) == 2
    assert desk_reservations == [reservation1, reservation2]
    assert desk_reservations[0].id == reservation1.id


# Test the list of reservations by user to not include past dates.
def test_list_reservations_by_user_past_dates(desk_reservation_service: DeskReservationService):

    reservation4 = DeskReservation(id=4, date=datetime.now() + timedelta(days=-1))
    reservation5 = DeskReservation(id=5, date=datetime.now() + timedelta(days=6))

    desk_reservation_service.create_desk_reservation(desk1, student1, reservation4)
    desk_reservation_service.create_desk_reservation(desk2, student2, reservation5)

    reservations = desk_reservation_service.list_desk_reservations_by_user(student2)
    assert len(reservations) == 1

