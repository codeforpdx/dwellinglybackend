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
    def setup(self):
        self.setup_fixture()

    def test_set_property_manager_raise_exception_when_id_not_found(self):
        with pytest.raises(ValidationError) as e:
            PropertyModel.set_property_managers([999])
        assert e.value.messages == ['999 is not a valid user id']

    def test_set_property_manager_raise_exception_when_user_not_manager(self):
        with pytest.raises(ValidationError) as e:
            PropertyModel.set_property_managers([self.admin.id])
        assert e.value.messages == ['{} is not a property manager'.format(self.admin.fullName)]

    def test_set_property_manager(self):
        expected = [UserModel.find_by_id(self.pm.id)]
        actual = PropertyModel.set_property_managers([self.pm.id])
        assert actual == expected

    def test_set_property_manger_with_no_ids_return_empty(self):
        assert PropertyModel.set_property_managers([]) == []

    def setup_fixture(self):
        self.pm = UserModel(
                email="manager@domain.com",
                password="asdf",
                firstName="Leslie",
                lastName="Knope",
                phone="505-503-4455",
                role=RoleEnum.PROPERTY_MANAGER,
                archived=False
            )
        self.pm.save_to_db()
        self.admin = UserModel(
                email="admin@dwellingly.com",
                password="asdf",
                firstName='firstName',
                lastName='lastName',
                phone="505-503-1111",
                role=RoleEnum.ADMIN,
                archived=False
            )
        self.admin.save_to_db()
        self.property = PropertyModel(
                name='the heights',
                address='111 SW Harrison',
                city="Portland",
                unit="101",
                state="OR",
                zipcode="97207",
                propertyManagerIDs=[self.pm.id],
                archived=False
            )
        self.property.save_to_db()
