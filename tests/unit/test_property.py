import pytest
from marshmallow import ValidationError
from models.property import PropertyModel
from models.user import UserModel


def test_set_property_manager_raise_exception_when_id_not_found(empty_test_db):
    with pytest.raises(ValidationError) as e:
        PropertyModel.set_property_managers([999])
    assert e.value.messages == ['999 is not a valid user id']


def test_set_property_manager_raise_exception_when_user_not_manager(test_database):
    with pytest.raises(ValidationError) as e:
        PropertyModel.set_property_managers([1])
    assert e.value.messages == ['user1 tester is not a property manager']


def test_set_property_manager(test_database):
    expected = [UserModel.find_by_id(5)]
    actual = PropertyModel.set_property_managers([5])
    assert actual == expected


def test_set_property_manger_with_no_ids_return_empty(empty_test_db):
    assert PropertyModel.set_property_managers([]) == []
