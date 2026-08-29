import sqlite3

def init_db():

    conn = sqlite3.connect("users.db")

    conn.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )

    """)
    conn.execute(
    """
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        action TEXT NOT NULL,

        image_name TEXT NOT NULL,

        date_time TEXT NOT NULL,

        status TEXT NOT NULL

    )
    """
)

    conn.commit()

    conn.close()