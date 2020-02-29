import datetime
import http.client
from schema import Schema


class Tester:

    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_PUT = "PUT"
    schemas = {}

    def __init__(self, api_url):
        self.api_url = api_url
        self.client = None

    def set_schema(self, endpoint, schema, method=METHOD_GET):

        if endpoint not in self.schemas.keys():
            self.schemas[endpoint] = {method: [Schema(schema)]}
        else:
            self.schemas[endpoint][method].append(Schema(schema))

    def execute_request(self, method, endpoint, schema, iter_order=None):

        # Generating data and starting HTTP client.

        payload = schema.execute(iter_order)
        client = http.client.HTTPConnection(self.api_url)

        # Starting timer and making the Request

        time = datetime.datetime.now()
        client.request(method, endpoint, payload, {"Content-type": "application/json"})

        # Stopping Timer.

        elapsed = (datetime.datetime.now() - time).total_seconds()

        # Building output.

        output = {"result": {"time_elapsed": elapsed, "result": client.getresponse().status}, "payload": payload}
        return output

    def run_all(self, iterations=100):
        for endpoint in self.schemas.keys():
            for method in self.schemas[endpoint].keys():

                results = []
                for index in range(iterations):

                    for schema in self.schemas[endpoint][method]:
                        results.append(self.execute_request(method, endpoint, schema, index))

                self.stats(results)


    def stats(self, results):

        total_time = 0.0
        error_requests = 0
        success_request = 0

        for result in results:
            total_time += result["result"]["time_elapsed"]
            if result["result"]["result"] == 200:
                success_request += 1
            else:
                error_requests += 1

        average_time_per_request = total_time / len(results)
        requests_per_second = len(results) / total_time

        print("Results: [TIME ELAPSED: %f] [REQUESTS PER SECOND: %f] [AVERAGE TIME PER REQUEST: %f]"
              " [SUCCESSFUL REQUESTS: %i] [ERROR REQUESTS: %i]" %
              (total_time, requests_per_second, average_time_per_request, success_request, error_requests))
