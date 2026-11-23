import pytest
import sqlite3
from app.main import app, DB_PATH, init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM comments")
    conn.execute("DELETE FROM posts")
    conn.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    with app.test_client() as client:
        yield client

def test_fallo_1_clave_secreta_segura():
    assert app.secret_key != "super_secret_vibe_key_12345"
    assert app.secret_key != "fallback_dev_key_only_for_tests"
    assert len(app.secret_key) >= 50

def test_fallo_2_contrasenas_hasheadas_en_db(client):
    from werkzeug.security import check_password_hash
    from app.main import get_db_connection
    raw_password = "PasswordSeguro2026!"
    response = client.post("/register", data={"username": "usuario_auditoria", "password": raw_password})
    assert response.status_code in (200, 302)
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", ("usuario_auditoria",)).fetchone()
    conn.close()
    assert user is not None
    assert user["password"] != raw_password
    assert check_password_hash(user["password"], raw_password) is True
