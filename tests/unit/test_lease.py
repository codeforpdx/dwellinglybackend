from models.lease import LeaseModel

def test_lease_initializes():
    lease = LeaseModel(0, 0, 0, 0, 0, 0, 0, 0)
    assert lease

