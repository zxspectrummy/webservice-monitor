import multiprocessing
from urllib.request import urlopen

import pytest

from exporter.exporter import start_http_server, PORT


@pytest.fixture(autouse=True, scope="session")
def start_server():
    p = multiprocessing.Process(target=start_http_server, args=())
    p.start()
    yield
    p.terminate()


def test_exporter_returns_target_status_code():
    with urlopen(f'http://localhost:{PORT}/probe?target=http://prometheus.io') as response:
        result = response.read().decode()
        assert 'http_status_code 200.0' in result
