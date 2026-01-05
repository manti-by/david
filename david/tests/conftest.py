import pytest

from django.test.client import Client


@pytest.fixture
def client():
    client = Client(HTTP_HOST="david.local")
    return client
