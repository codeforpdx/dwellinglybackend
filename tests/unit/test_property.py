import pytest
from tests.unit.base_interface_test import BaseInterfaceTest
from models.property import PropertyModel
from schemas.property import PropertySchema
from db import db


class TestBasePropertyModel(BaseInterfaceTest):
    def setup(self):
        self.object = PropertyModel()
        self.custom_404_msg = 'Property not found'
        self.schema = PropertySchema


@pytest.mark.usefixtures('empty_test_db')
class TestProperty:
    def test_property_created_with_manager_ids(self, property_attributes, create_property_manager):
        property_attrs = property_attributes()
        pm_1 = create_property_manager()
        pm_2 = create_property_manager()
        property_attrs['propertyManagerIDs'] = [
            pm_1.id,
            pm_2.id
        ]

        prop = PropertyModel.create(schema=PropertySchema, payload=property_attrs)
        db.session.rollback()

        assert prop
        assert prop.managers == [pm_1, pm_2]

    def test_manager_update(self, create_property, create_property_manager):
        prop = create_property()
        pm_1 = prop.managers[0]
        pm_2 = create_property_manager()
        pm_3 = create_property_manager()
        payload = { 'propertyManagerIDs': [pm_2.id, pm_3.id] }

        PropertyModel.update(schema=PropertySchema, id=prop.id, payload=payload)
        db.session.rollback()

        assert prop.managers == [pm_2, pm_3]
