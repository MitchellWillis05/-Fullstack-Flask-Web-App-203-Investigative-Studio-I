# import sqlite3 for database interaction
import sqlite3
import password_handler as ph


# database connection method
def db_connect():
    conn = None
    try:
        conn = sqlite3.connect("user_database.db")
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
    return conn


def create_new_entry(userid, title, mood, color, content, date):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO journal (userid, title, mood, color, content, date) VALUES (?, ?, ?, ?, ?, ?)",
            (userid, title, mood, color, content, date)
        )
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False
    finally:
        cur.close()
        conn.close()


def fetch_entries_by_id(userid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT entryid, userid, title, mood, color, content, date FROM journal WHERE userid = ?",
                    (userid,))
        data_fetched = cur.fetchall()
        return data_fetched
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    except IndexError as error:
        print(error)
        return None
    finally:
        cur.close()
        conn.close()
