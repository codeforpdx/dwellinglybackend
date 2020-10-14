from conftest import newPropertyName, newPropertyAddress

def test_new_property(new_property, empty_database):
    assert new_property.name == newPropertyName
    assert new_property.address == newPropertyAddress