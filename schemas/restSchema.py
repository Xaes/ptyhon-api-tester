from schemas.schema import BaseSchema


class RestSchema(BaseSchema):

    def __init__(self, schema):
        self.schema = schema

    def to_string(self):
        return {"schema": self.schema}
