class TestSerialize:
    def test_serialize(self, create_property_manager):
        property_manager = create_property_manager()
        assert property_manager.serialize() == {"properties": []}
