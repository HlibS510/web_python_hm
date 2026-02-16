import sqlite3


DB_NAME = "data.db"
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row

conn.executemany("""
            INSERT INTO sections (name, slug)
            VALUES (?, ?)""",
                 [("Lifestyle", "lifestyle"),
                  ("Food", "food"),
                  ("Tutorials", "tutorials"),
                  ("Travel", "travel"),
                  ("News", "news"),
                  ("Gaming", "gaming"),
                  ("Questions", "questions"),
                  ("Technology", "technology")],
                 )
conn.commit()
conn.close()
