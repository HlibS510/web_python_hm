import sqlite3


DB_NAME = "data.db"
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row

conn.executemany("""
            INSERT INTO sections (name, slug)
            VALUES (?, ?)""",
                 [("Мої гоббі", "my-hobbies"),
                  ("Керамічні вироби", "ceramics"),
                  ("Аніме", "anime")],
                 )
conn.commit()
conn.close()
