import time
import random
import requests
from prometheus_client import start_http_server, Gauge

HTTP_STATUS_CODE = Gauge('http_status_code', "HTTP Status Code")

url = ''


def get_metrics():
    try:
        HTTP_STATUS_CODE.set(requests.get(url).status_code)
    except requests.exceptions.ConnectionError:
        HTTP_STATUS_CODE.set(0)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        get_metrics()
        time.sleep(random.randrange(1, 10))
