from faker import Faker


class BaseSchema:

    _faker = Faker()

    @staticmethod
    def generate_data(data_schema, iter_order=None):

        generated_record = {}

        # Generating Fake Data.

        for attribute in data_schema.keys():

            attr_obj = data_schema[attribute]
            has_default = "default_value" in attr_obj.keys()

            # Generate recursive ID if data type is recursive_id.

            if not has_default and attr_obj["data_type"] == "recursive_id":
                fake_data = BaseSchema.generate_recursive_id(iter_order)

            else:

                if has_default:
                    fake_data = attr_obj["default_value"]
                elif "parameters" in attr_obj.keys():
                    fake_data = getattr(BaseSchema._faker, attr_obj["data_type"])(**attr_obj["parameters"])
                else:
                    fake_data = getattr(BaseSchema._faker, attr_obj["data_type"])()

            # Applying lambda if there is one.

            generated_record[attribute] = attr_obj["transform"](fake_data) if "transform" in attr_obj.keys() else fake_data

        return generated_record

    @staticmethod
    def generate_recursive_id(iter_order):

        if iter_order is None:
            raise ValueError("You can't have a procedural ID generation without exposing iteration order.")

        # Choosing ID's used for relation (ID must already exist on DB).

        fake_data = BaseSchema._faker.pyint(min_value=1, max_value=iter_order + 1, step=1) if iter_order > 1 else None

        if fake_data is not None and fake_data == iter_order:
            fake_data -= 1

        return fake_data
