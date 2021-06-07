import pytest
from unittest.mock import patch
from db import db
from nobiru.nobiru_list import NobiruList
from models.base_model import BaseModel
from werkzeug.exceptions import NotFound


class DummyRelationModel(BaseModel):
    __tablename__ = "fake_relations"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    fake_id = db.Column(db.Integer, db.ForeignKey("fakes.id"), nullable=False)


class DummyModel(BaseModel):
    __tablename__ = "fakes"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))

    values = db.relationship(
        DummyRelationModel,
        backref="fake",
        lazy=False,
        cascade="all, delete-orphan",
        collection_class=NobiruList,
    )


@pytest.mark.usefixtures("empty_test_db")
class TestFunctionalNobiruList:
    def create_fake_model(self):
        fake = DummyModel()
        fake.values.append(DummyRelationModel())
        db.session.add(fake)
        db.session.commit()
        return fake

    def test_create_fake_model(self):
        fake = self.create_fake_model()
        assert DummyModel.query.all() == [fake]

    @patch.object(db, "session")
    def test_delete(self, mock_session):
        fake = self.create_fake_model()
        value = fake.values[0]

        with patch.object(fake.values, "remove") as mock_remove:
            fake.values.delete(value)

        mock_remove.assert_called_once_with(value)
        mock_session.commit.assert_called()

    def test_delete_with_non_existant_entity(self):
        fake = self.create_fake_model()
        other_fake = self.create_fake_model()
        other_value = other_fake.values[0]

        with pytest.raises(NotFound) as err:
            fake.values.delete(other_value)

        assert (
            err.exconly()
            == "werkzeug.exceptions.NotFound: 404 Not Found: DummyRelation not found"
        )
