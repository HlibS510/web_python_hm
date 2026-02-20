import sqlite3

DB_NAME = "loggins.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("CREATE TABLE IF NOT EXISTS logins(name TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
        db.commit()

def create_new_account(name, password):
    with get_db() as db:
        user = db.execute("INSERT INTO IF NOT EXISTS logins (name, password) VALUES (?, ?)", (name, password))
        db.commit()
    if user:
        return True
    else:
        return False

def login_user(name, password):
    with get_db() as db:
        user = db.execute("SELECT * FROM logins WHERE name = ? AND password = ?",(name, password)).fetchone()
        db.commit()
    if user:
        return True
    else:
        return False

init_db()