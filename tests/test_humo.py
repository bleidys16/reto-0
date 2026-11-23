import pytest
from app.main import app, init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    with app.test_client() as client:
        yield client

def test_humo_arranque_aplicacion(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Entradas del Blog" in response.data
