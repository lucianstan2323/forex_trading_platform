import pytest
import requests

@pytest.fixture
def client():
    with requests.Session() as session:
        yield session

def pytest_addoption(parser):
    parser.addoption(
        "--api-url", action="store", default="http://api-server:8081", help="URL for the API"
    )

@pytest.fixture
def base_url(request):
    return request.config.getoption("--api-url")
