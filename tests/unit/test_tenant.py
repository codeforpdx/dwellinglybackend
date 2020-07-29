from models.tenant import TenantModel

firstName = "Renty"
lastName = "McRenter"
phone = "800-RENT-ALOT"
propertyID = 1
staffIDs = [1, 2]


def test_tenant(test_database):
    newTenant = TenantModel(firstName=firstName, lastName=lastName,
                            phone=phone, propertyID=propertyID, staffIDs=staffIDs)
    assert newTenant.firstName == firstName
    assert newTenant.lastName == lastName
    assert newTenant.phone == phone
    assert newTenant.propertyID == propertyID
