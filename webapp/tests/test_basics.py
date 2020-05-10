import pytest

from webapp import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as c:
        yield c


def test_start(client):
    assert client.get("/").status_code == 200


def test_registration_page(client):
    assert client.get("/users/register").status_code == 200


def test_login_page(client):
    assert client.get("/users/login").status_code == 200
