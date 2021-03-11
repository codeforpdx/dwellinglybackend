import pytest
from models.lease import LeaseModel
from schemas.lease import LeaseSchema
from serializers.lease import LeaseSerializer
from unittest.mock import patch


@pytest.mark.usefixtures("client_class", "empty_test_db")
class TestLease:
    def setup(self):
        self.endpoint = "/api/lease"

    def test_get_a_lease(self, valid_header, create_lease):
        lease = create_lease()
        with patch.object(LeaseModel, "find", return_value=lease) as mock_find:
            response = self.client.get(f"{self.endpoint}/1", headers=valid_header)

        mock_find.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == LeaseSerializer.serialize(lease)

    def test_get_all_leases(self, valid_header, create_lease):
        lease = create_lease()
        second_lease = create_lease()

        response = self.client.get(self.endpoint, headers=valid_header)

        assert response.status_code == 200
        assert response.json == {
            "leases": [
                LeaseSerializer.serialize(lease),
                LeaseSerializer.serialize(second_lease),
            ]
        }

    def test_get_all_leases_when_no_leases(self, valid_header):
        response = self.client.get(self.endpoint, headers=valid_header)

        assert response.status_code == 200
        assert response.json == {"leases": []}

    def test_create_lease(self, valid_header):
        with patch.object(LeaseModel, "create") as mock_create:
            response = self.client.post(
                self.endpoint, json={"yes": "ok"}, headers=valid_header
            )

        mock_create.assert_called_once_with(schema=LeaseSchema, payload={"yes": "ok"})
        assert response.status_code == 201
        assert response.json == {"message": "Lease created successfully"}

    def test_delete_lease(self, valid_header):
        with patch.object(LeaseModel, "delete") as mock_delete:
            response = self.client.delete(f"{self.endpoint}/1", headers=valid_header)

        mock_delete.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.json == {"message": "Lease deleted"}

    def test_update_lease(self, valid_header, create_lease):
        lease = create_lease()
        with patch.object(LeaseModel, "update", return_value=lease) as mock_update:
            response = self.client.put(
                f"{self.endpoint}/1", json={"hello": "world"}, headers=valid_header
            )

        mock_update.assert_called_once_with(
            schema=LeaseSchema, id=1, payload={"hello": "world"}
        )
        assert response.status_code == 200
        assert response.json == LeaseSerializer.serialize(lease)
