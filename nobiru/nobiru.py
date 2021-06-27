class Nobiru:
    @staticmethod
    def json(collection, **kwargs):
        return [object.json(**kwargs) for object in collection]
