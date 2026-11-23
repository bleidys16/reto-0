import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
_env_key = os.environ.get("SECRET_KEY", "")
if len(_env_key) >= 50 and _env_key not in ("super_secret_vibe_key_12345", "fallback_dev_key_only_for_tests"):
    app.secret_key = _env_key
else:
    import secrets
    app.secret_key = secrets.token_hex(32)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "blog.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL, author TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER NOT NULL, author TEXT NOT NULL, content TEXT NOT NULL, FOREIGN KEY (post_id) REFERENCES posts (id))''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        try:
            hashed_password = generate_password_hash(password)
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "El usuario ya existe", 400
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            return redirect(url_for("index"))
        return "Credenciales inválidas", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        conn = get_db_connection()
        conn.execute("INSERT INTO posts (title, content, author) VALUES (?, ?)", (title, content, session["username"]))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("new_post.html")

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not post:
        conn.close()
        abort(404)
    if request.method == "POST":
        content = request.form.get("content")
        author = session.get("username", "Anónimo")
        conn.execute("INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)", (post_id, author, content))
        conn.commit()
    comments = conn.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY id ASC", (post_id,)).fetchall()
    conn.close()
    return render_template("post.html", post=post, comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
