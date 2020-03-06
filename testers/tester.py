class BaseTester:

    # API Types.

    API_REST = "API_REST"
    API_GQL = "API_GQL"

    # Default Values.

    DEFAULT_ITERATIONS = 100

    @staticmethod
    def stats(results):

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
