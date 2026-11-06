import base64

import pytest
from werkzeug.security import generate_password_hash

from app import create_app


@pytest.fixture
def app(tmp_path):
    application = create_app(str(tmp_path / "test.db"))
    application.config["TESTING"] = True
    # Синтетические учётные записи только для тестов
    application.config["USERS"] = {
        "alice": generate_password_hash("alice-test-pass"),
        "bob": generate_password_hash("bob-test-pass"),
    }
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def basic(username: str, password: str) -> dict:
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


@pytest.fixture
def alice():
    return basic("alice", "alice-test-pass")


@pytest.fixture
def bob():
    return basic("bob", "bob-test-pass")
