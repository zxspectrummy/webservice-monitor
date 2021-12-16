import urllib.parse
from http.server import HTTPServer

import requests
from prometheus_client import Gauge, MetricsHandler

HTTP_STATUS_CODE = Gauge('http_status_code', "HTTP Status Code")


class RequestHandler(MetricsHandler):
    def do_GET(self):

        parsed_path = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        print(self.path, query)

        if "target" in query:
            endpoint = query['target'][0]

            try:
                http_status_code = requests.get(endpoint).status_code
                HTTP_STATUS_CODE.set(http_status_code)
            except requests.exceptions.ConnectionError:
                HTTP_STATUS_CODE.set(0)
            return super(RequestHandler, self).do_GET()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"No target defined\n")


if __name__ == '__main__':
    server_address = ('', int(8000))
    HTTPServer(server_address, RequestHandler).serve_forever()

