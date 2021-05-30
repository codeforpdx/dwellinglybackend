class Nobiru:
    @staticmethod
    def json(collection):
        return [object.json() for object in collection]
