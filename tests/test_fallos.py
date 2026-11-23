import pytest
import sqlite3
from werkzeug.security import check_password_hash
from app.main import app, DB_PATH, get_db_connection, init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    # Limpiar base de datos para pruebas
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM comments")
    conn.execute("DELETE FROM posts")
    conn.execute("DELETE FROM users")
    try:
        conn.execute("DELETE FROM sqlite_sequence")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
    with app.test_client() as client:
        yield client

def test_fallo_1_clave_secreta_segura():
    """Fallo 1 (Criterio 4 - Secretos y claves):
    La clave secreta de sesión no debe ser una clave quemada, ni un fallback débil,
    y debe cumplir con una longitud criptográfica mínima de 50 caracteres para evitar ataques de falsificación de sesión.
    """
    assert app.secret_key != "super_secret_vibe_key_12345"
    assert app.secret_key != "fallback_dev_key_only_for_tests"
    assert len(app.secret_key) >= 50

def test_fallo_2_contrasenas_hasheadas_en_db(client):
    """Fallo 2 (Criterio 3 - Contraseñas y hash):
    Al registrar un usuario, la contraseña no debe almacenarse en texto plano en la base de datos.
    Debe persistirse utilizando un hash seguro (PBKDF2/scrypt con salt) verificable con check_password_hash.
    """
    raw_password = "PasswordSeguro2026!"
    response = client.post("/register", data={"username": "usuario_auditoria", "password": raw_password})
    assert response.status_code in (200, 302)

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", ("usuario_auditoria",)).fetchone()
    conn.close()

    assert user is not None
    # Debe fallar si la contraseña se almacena en texto claro
    assert user["password"] != raw_password
    assert check_password_hash(user["password"], raw_password) is True

def test_fallo_3_rechazo_comentarios_vacios(client):
    """Fallo 3 (Criterio 2 - Validación de entradas):
    No se deben permitir comentarios vacíos ni compuestos únicamente por espacios en blanco.
    La aplicación debe responder con HTTP 400 Bad Request y no insertar registros en blanco en la base de datos.
    """
    # Crear post previo
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
        ("Entrada de Prueba", "Contenido para validar comentarios", "autor_prueba")
    )
    conn.commit()
    conn.close()

    # Enviar comentario inválido (solo espacios en blanco)
    response = client.post("/post/1", data={"content": "     "})
    assert response.status_code == 400

    # Verificar en base de datos que no se guardó ningún comentario vacío
    conn = get_db_connection()
    total_comments = conn.execute("SELECT COUNT(*) as total FROM comments WHERE post_id = 1").fetchone()["total"]
    conn.close()
    assert total_comments == 0
