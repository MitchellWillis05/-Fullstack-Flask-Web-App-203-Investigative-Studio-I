# import sqlite3 for database interaction
import sqlite3


# database connection method
def db_connect():
    conn = None
    try:
        conn = sqlite3.connect("user_database.db")
    except sqlite3.Error as error:
        print(error.sqlite_errorcode)
        print(error.sqlite_errorname)
    return conn


def check_unique_cred(username, email):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM user WHERE username = ? OR email = ?", (username, email))
        results = cur.fetchall()
        if len(results) == 0:
            return True
        else:
            return False
    finally:
        cur.close()
        conn.close()


# Current user class which holds the current user's data
# @singleton
class CurrentUser:
    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

