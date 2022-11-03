import pytest

from server import config_app


@pytest.fixture
def client():
    app = config_app({"TESTING": True})
    with app.test_client() as client:
        yield client
