class InvalidRequest(Exception):
    def __init__(self, status_code, description):
        Exception.__init__(self)
        self.status_code = status_code
        self.description = description

    def to_dict(self):
        return {"message": self.description}
