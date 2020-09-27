from unittest.mock import patch
from db import db


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

    def test_find(self):
        class_name = self.object.__class__.__name__
        with patch.object(self.object.__class__, 'query') as mock_query:
            self.object.__class__.find(1)

        mock_query.get_or_404.assert_called_with(1, f"{class_name} not found")

    def test_json(self):
        with patch.object(self.object, 'json') as mock_json:
            self.object.json()

        mock_json.assert_called()
