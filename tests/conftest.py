import pytest
import requests

@pytest.fixture
def client():
    with requests.Session() as session:
        yield session
