from gql import gql
from string import Template

from schemas.schema import BaseSchema


class GQLSchema(BaseSchema):

    MUTATION_TYPE = "MUTATION_TYPE"
    QUERY_TYPE = "QUERY_TYPE"

    def __init__(self, query, data_schema, query_type=QUERY_TYPE):
        self.query = query
        self.data_schema = data_schema
        self.query_type = query_type

    def prepare_query(self, payload):

        # If there is no payload, just convert the query to GQL.

        if not payload:
            return gql(self.query)

        # Map the payload with the query and convert to GQL.

        mapped_query = Template(self.query).safe_substitute(**payload)
        return gql(mapped_query)
