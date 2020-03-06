import datetime

from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from schemas.gqlSchema import GQLSchema
from testers.tester import BaseTester


class GQLTester(BaseTester):

    def __init__(self, url):

        # Defining Info.

        self.url = url
        self.api_type = self.API_GQL

        # Schemas.

        self.login_data = {
            "schema": None,
            "token": {"expires_in": 0, "token": None},
            "credentials": {"username": None, "password": None}
        }

        self.schemas = []

        # Initializing GQL Client.

        self.transport_headers = {}
        self.client = Client(transport=self._generate_transport())

    def set_login(self, query, username, password):
        self.login_data["schema"] = GQLSchema(query, None, GQLSchema.MUTATION_TYPE)
        self.login_data["credentials"]["username"] = username
        self.login_data["credentials"]["password"] = password

    def login(self):

        if not self.login_data["schema"]:
            raise ValueError("Can't login without a login schema.")

        if not self.client:
            raise ValueError("Can't execute login without a client set.")

        if not self.login_data["credentials"]["username"] and not self.login_data["credentials"]["password"]:
            raise ValueError("Credentials are missing.")

        gql_query = self.login_data["schema"].prepare_query(self.login_data["credentials"])
        result = self.client.execute(gql_query)

        # Setting Results.

        self.login_data["token"]["expires_in"] = result["login"]["expires_in"]
        self.login_data["token"]["token"] = "Bearer " + result["login"]["token"]
        self.transport_headers = {'Authorization': self.login_data["token"]["token"]}

        # Setting a new Transport Header.

        self.client.transport = self._generate_transport()

    def set_schema(self, query, data_schema=None, query_type=GQLSchema.QUERY_TYPE):
        self.schemas.append(GQLSchema(query, data_schema, query_type))

    def execute_request(self, schema, iter_order=None):

        # Generating data and mapping it.

        payload = schema.generate_data(schema.data_schema, iter_order)

        # Starting timer and making the Request

        time = datetime.datetime.now()
        self.client.execute(schema.prepare_query(payload))

        # Stopping Timer.

        elapsed = (datetime.datetime.now() - time).total_seconds()

        output = {"result": {"time_elapsed": elapsed, "payload": payload, "result": 200}}
        return output

    def run_all(self, iterations=BaseTester.DEFAULT_ITERATIONS):

        results = []

        # Login in if schema is present.

        if self.login_data["schema"]:
            self.login()

        # Executing Schemas.

        for schema in self.schemas:
            for index in range(iterations):
                results.append(self.execute_request(schema, index))

        self.stats(results)

    def _generate_transport(self):
        return RequestsHTTPTransport(
            url=self.url,
            use_json=True,
            headers=self.transport_headers
        )
