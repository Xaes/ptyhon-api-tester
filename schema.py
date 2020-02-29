import json
from faker import Faker
fake = Faker()


class Schema:

    def __init__(self, schema):
        self.schema = schema

    def execute(self, iter_order=None):

        generated_record = {}

        # Generating Fake Data.

        for attribute in self.schema.keys():

            attr_obj = self.schema[attribute]
            has_default = "default_value" in attr_obj.keys()

            if not has_default and attr_obj["data_type"] == "recursive_relation":

                if iter_order is None:
                    raise ValueError("You can't have a procedural ID generation without exposing iteration order.")

                # Choosing ID's used for relation (ID must already exist on DB).

                fake_data = fake.pyint(min_value=1, max_value=iter_order+1, step=1) if iter_order > 1 else None

                if fake_data is not None and fake_data == iter_order:
                    fake_data -= 1

            else:
                fake_data = attr_obj["default_value"] if has_default else getattr(fake, attr_obj["data_type"])()

            # Applying lambda if there is one.

            generated_record[attribute] = attr_obj["transform"](fake_data) if "transform" in attr_obj.keys() else fake_data

        return json.dumps(generated_record)

    def to_string(self):
        return {"schema": self.schema}
