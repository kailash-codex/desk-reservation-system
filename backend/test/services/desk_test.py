import pytest

from sqlalchemy.orm import Session

from ...models import User, Desk, Role
from ...entities import UserEntity, DeskEntity, RoleEntity, PermissionEntity
from ...services import DeskService, PermissionService, UserPermissionError

# Mock Models #
# Desks
desk1 = Desk(id=1, tag='AA1', desk_type='Computer Desk', included_resource='Pro Display XDR w/ Mac Pro', available=True)
desk2 = Desk(id=2, tag='CD1', desk_type='Standing Desk', included_resource='Windows Desktop i9', available=True)

# Root User
root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu')
root_role = Role(id=1, name='root')

# Student User
student1 = User(id=2, pid=123456789, onyen='student1', email='student1@unc.edu')
student2 = User(id=3, pid=987654321, onyen='student2', email='student2@unc.edu')


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

    # Bootstrap for Student User
    student1_entity = UserEntity.from_model(student1)
    student2_entity = UserEntity.from_model(student2)

    test_session.add(student1_entity)
    test_session.add(student2_entity)

    test_session.commit()

    # Bootstrap for Desks
    desk1_entity = DeskEntity.from_model(desk1)
    desk2_entity = DeskEntity.from_model(desk2)

    test_session.add(desk1_entity)
    test_session.add(desk2_entity)

    test_session.commit()

    yield


# pytest fixture to use for all the tests.
@pytest.fixture()
def permission(test_session: Session):
    return PermissionService(test_session)

@pytest.fixture()
def desk_service(test_session: Session, permission: PermissionService):
    return DeskService(test_session, permission)


# Test listing all desks in the database.
def test_list_all_desks(desk_service: DeskService):
    desk_service._permission.enforce(root, 'admin/', '*')
    desks = desk_service.list_all_desks(root)
    
    assert [desk.tag for desk in desks] == ['AA1', 'CD1']

# Test listing all desks in the database AS a student.
def test_list_all_desks_as_student(desk_service: DeskService):
    with pytest.raises(UserPermissionError):
        desk_service.list_all_desks(student1)


# Test toggleing the desk availability (for Admin).
def test_toggle_desk_availability(desk_service: DeskService):
    desk_service._permission.enforce(root, 'admin/', '*')

    desk_toggle = desk_service.toggle_desk_availability(desk1, root)
    assert not desk_toggle.available

    desk_toggle = desk_service.toggle_desk_availability(desk1, root)
    assert desk_toggle.available

# Test to create new desk (Admin).
def test_create_desk(desk_service: DeskService):
    desk3 = Desk(id=3, tag='ND1', desk_type='Standing Desk', included_resource='iMac w/ Pro Display', available=True)

    desk_service._permission.enforce(root, 'admin/', '*')

    new_desk = desk_service.create_desk(desk3, root)
    assert new_desk.tag == desk3.tag
    assert new_desk is not None


# Test for Student trying to create a new desk.
def test_create_desk_as_student(desk_service: DeskService):
    desk3 = Desk(id=3, tag='ND1', desk_type='Standing Desk', included_resource='iMac w/ Pro Display', available=True)

    with pytest.raises(UserPermissionError):
        desk_service.create_desk(desk3, student1)


# Test for Second Student trying to create a new desk.
def test_create_desk_as_student(desk_service: DeskService):
    desk4 = Desk(id=4, tag='ND4', desk_type='Standing Desk', included_resource='iMac w/ Pro Display', available=True)

    with pytest.raises(UserPermissionError):
        desk_service.create_desk(desk4, student2)


# Test to remove a desk.
def test_remove_desk(desk_service: DeskService):
    desk_service._permission.enforce(root, 'admin/', '*')

    removed_desk1 = desk_service.remove_desk(desk1, root)
    assert removed_desk1.tag == desk1.tag
    assert removed_desk1 is not None


# Test of Student 1 removing a desk.
def test_remove_desk_as_student(desk_service: DeskService):
    with pytest.raises(UserPermissionError):
        desk_service.remove_desk(desk1, student1)


# Test of Student 2 removing a desk.
def test_remove_desk_as_student(desk_service: DeskService):
    with pytest.raises(UserPermissionError):
        desk_service.remove_desk(desk2, student2)
    

# Test update Desk.
def test_update_desk(desk_service: DeskService):
    desk5 = Desk(id=5, tag='BD1', desk_type='Computer Desk', included_resource='Pro Display XDR w/ Mac Pro', available=True)
    desk_service._permission.enforce(root, 'admin/', '*')
    create_desk = desk_service.create_desk(desk5, root)

    desk5_update = Desk(id=5, tag='BD1', desk_type='Standing Desk', included_resource='Windows Desktop i9', available=False)

    desk_service.update_desk(desk5.id, desk5_update, root)
    assert create_desk.id == desk5_update.id
    assert desk5_update.tag == 'BD1'
    assert desk5_update.desk_type == 'Standing Desk'


# Test update Desk as a student.
def test_update_desk_as_student(desk_service: DeskService):
    updated_desk = Desk(id=2, tag='CD1', desk_type='Computer Desk', included_resource='Windows Desktop i5', available=True)
    with pytest.raises(UserPermissionError):
        desk_service.update_desk(desk2.id, updated_desk, student1)
