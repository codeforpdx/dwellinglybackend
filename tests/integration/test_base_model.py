import pytest

from ma import ma
from db import db
from models.base_model import BaseModel
from tests.unit.base_interface_test import BaseInterfaceTest


class DummyModel(BaseModel):
    __tablename__ = "fake"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))

class DummySchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = DummyModel

class TestDummyModel(BaseInterfaceTest):
    def setup(self):
        self.object = DummyModel(**{'first_name': 'Bye'})
        self.schema = DummySchema
        self.custom_404_msg = "Dummy not found"

@pytest.mark.usefixtures('empty_test_db')
class TestUpdate:
    def setup(self):
        db.session.add(DummyModel(**{'first_name': 'Bye'}))
        db.session.commit()
        self.id = DummyModel.query.first().id

    def test_partial_update(self):
        DummyModel.update(DummySchema, self.id, {'last_name': 'World'})
        obj = DummyModel.query.first()

        assert obj.first_name == 'Bye'
        assert obj.last_name == 'World'
        assert obj.updated_at != None

    def test_full_update(self):
        DummyModel.update(DummySchema, self.id, {'first_name': 'Hello', 'last_name': 'World'})
        obj = DummyModel.query.first()

        assert obj.first_name == 'Hello'
        assert obj.last_name == 'World'
        assert obj.updated_at != None

    def test_no_update(self):
        DummyModel.update(DummySchema, self.id, {})
        obj = DummyModel.query.first()

        assert obj.first_name == 'Bye'
        assert obj.last_name == None
        assert obj.updated_at == None


@pytest.mark.usefixtures('empty_test_db')
class TestCreate:
    def test_it_returns_the_created_object(self):
        obj = DummyModel.create(DummySchema, {'first_name': 'Hello'})

        assert obj.id != None
