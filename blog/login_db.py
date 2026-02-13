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

def add_money(name, money):
    with get_db() as db:
        db.execute("UPDATE logins SET money = money + ? WHERE name = ?", (money, name))
        db.commit()

def create_new_account(name, password):
    try:
        with get_db() as db:
            db.execute("INSERT INTO logins (name, password) VALUES (?, ?)", (name, password))
            db.commit()
    except:
        print("Error")

def login(name, password):
    with get_db() as db:
        user = db.execute("SELECT * FROM logins WHERE name = ? AND password = ?",(name, password)).fetchone()
        db.commit()
    if user:
        return True
    else:
        return False

init_db()