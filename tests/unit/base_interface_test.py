import pytest
from unittest.mock import patch
from unittest import mock
from db import db
from marshmallow import ValidationError, EXCLUDE
from werkzeug.exceptions import BadRequest


@pytest.mark.usefixtures('empty_test_db')
class BaseInterfaceTest:
    @patch.object(db, 'session')
    def test_save_to_db(self, mock_session):
        self.object.save_to_db()

        mock_session.add.assert_called_with(self.object)
        mock_session.commit.assert_called()

    @patch.object(db, 'session')
    def test_delete_from_db(self, mock_session):
        self.object.delete_from_db()

        mock_session.delete.assert_called_with(self.object)
        mock_session.commit.assert_called()

    @patch.object(db, 'session')
    def test_delete(self, mock_session):
        with patch.object(self.object.__class__, 'find', return_value=self.object) as mock_find:
            self.object.__class__.delete(1)

        mock_find.assert_called()

        mock_session.delete.assert_called_with(self.object)
        mock_session.commit.assert_called()

    def test_find(self):
        with patch.object(self.object.__class__, 'query') as mock_query:
            self.object.__class__.find(1)

        mock_query.get_or_404.assert_called_with(1, self.custom_404_msg)

    @patch.object(db, 'session')
    def test_create(self, mock_session):
        with patch.object(self.object.__class__, 'validate', return_value={}) as mock_validate:
            response = self.object.__class__.create(self.schema, {})

        mock_validate.assert_called_with(self.schema, {})

        mock_session.add.assert_called()
        mock_session.commit.assert_called()

        assert response

    @patch.object(db, 'session')
    def test_create_with_invalid_attributes(self, mock_session):
        validation_error = mock.Mock()
        validation_error.side_effect = ValidationError(message='Invalid attributes', field_name='foo')
        with patch.object(self.schema, 'load', validation_error):
            with pytest.raises(BadRequest):
                self.object.__class__.create(self.schema, {})

    @patch.object(db, 'session')
    def test_update(self, mock_session):
        with patch.object(self.object.__class__, 'find', return_value=self.object) as mock_find:
            with patch.object(self.object.__class__, 'validate', return_value={}) as mock_validate:
                response = self.object.__class__.update(self.schema, 1, {})

        mock_find.assert_called_with(1)
        mock_validate.assert_called_with(self.schema, {}, partial=True)
        mock_session.add.assert_called_with(self.object)
        mock_session.commit.assert_called()

        assert response == self.object

    @patch.object(db, 'session')
    def test_update_with_validation_errors(self, mock_session):
        validation_error = mock.Mock()
        validation_error.side_effect = ValidationError(message='Invalid attributes', field_name='foo')
        with patch.object(self.object.__class__, 'find', return_value=self.object) as mock_find:
            with patch.object(self.schema, 'load', validation_error):
                with pytest.raises(BadRequest):
                    self.object.__class__.update(self.schema, 1, {})

    @patch.object(db, 'session')
    def test_validate_with_valid_attributes(self, mock_session):
        with patch.object(self.schema, 'load', return_value={}) as mock_load:
            response = self.object.__class__.validate(self.schema, {})

        mock_load.assert_called_with({}, unknown=EXCLUDE, partial=False)

        assert response == {}
