import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from marshmallow import ValidationError
from models.property import PropertyModel
from models.user import UserModel, RoleEnum
from schemas.property import PropertySchema


class TestBasePropertyModel(BaseInterfaceTest):
    def setup(self):
        self.object = PropertyModel()
        self.custom_404_msg = 'Property not found'
        self.schema = PropertySchema


@pytest.mark.usefixtures('empty_test_db')
class TestPropertyModel:
    def test_set_property_manager_raise_exception_when_id_not_found(self):
        with pytest.raises(ValidationError) as e:
            PropertyModel.set_property_managers([999])
        assert e.value.messages == ['999 is not a valid user id']

    def test_set_property_manager_raise_exception_when_user_not_manager(self, create_admin_user):
        admin = create_admin_user()
        with pytest.raises(ValidationError) as e:
            PropertyModel.set_property_managers([admin.id])
        assert e.value.messages == ['{} is not a property manager'.format(admin.fullName)]

    def test_set_property_manager(self, create_property_manager):
        pm = create_property_manager()
        expected = [pm]
        actual = PropertyModel.set_property_managers([pm.id])
        assert actual == expected

    def test_set_property_manger_with_no_ids_return_empty(self):
        assert PropertyModel.set_property_managers([]) == []
