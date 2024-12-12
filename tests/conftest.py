import pytest
import requests

@pytest.fixture
def client():
    with requests.Session() as session:
        yield session

def pytest_addoption(parser):
    parser.addoption(
        "--base-url", action="store", default="http://localhost:8081", help="Base URL for the API"
    )

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")
