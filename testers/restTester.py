import datetime
import http.client
import json

from schemas.restSchema import RestSchema
from .tester import BaseTester


class RestAPITester(BaseTester):

    # Method Types.

    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_PUT = "PUT"
    METHOD_DELETE = "DELETE"

    def __init__(self, api_url):
        self.api_url = api_url
        self.api_type = self.API_REST
        self.schemas = {}

    def set_schema(self, endpoint, schema, method=METHOD_POST):

        if endpoint not in self.schemas.keys():
            self.schemas[endpoint] = {method: [RestSchema(schema)]}
        else:
            self.schemas[endpoint][method].append(RestSchema(schema))

    def execute_request(self, method, endpoint, schema, iter_order=None):

        # Generating data and starting HTTP client.

        payload = json.dumps(schema.generate_data(schema, iter_order))
        client = http.client.HTTPConnection(self.api_url)

        # Starting timer and making the Request

        time = datetime.datetime.now()
        client.request(method, endpoint, payload, {"Content-type": "application/json"})

        # Stopping Timer.

        elapsed = (datetime.datetime.now() - time).total_seconds()

        # Building output.

        output = {"result": {"time_elapsed": elapsed, "result": client.getresponse().status}, "payload": payload}
        return output

    def run_all(self, iterations=BaseTester.DEFAULT_ITERATIONS):
        for endpoint in self.schemas.keys():
            for method in self.schemas[endpoint].keys():

                results = []
                for index in range(iterations):

                    for schema in self.schemas[endpoint][method]:
                        results.append(self.execute_request(method, endpoint, schema, index))

                self.stats(results)
