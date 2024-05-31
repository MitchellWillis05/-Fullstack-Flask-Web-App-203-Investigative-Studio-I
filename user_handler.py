# import sqlite3 for database interaction
import sqlite3
import password_handler as ph


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
        cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        results_u = cur.fetchall()
        cur.execute("SELECT * FROM user WHERE email = ?", (email.lower(),))
        results_e = cur.fetchall()
        if len(results_u) == 0:
            if len(results_e) == 0:
                return 2
            else:
                return 1
        else:
            return 0
    finally:
        cur.close()
        conn.close()


def create_new_user(username, email, password):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO user (username, email, password) VALUES (?,?,?)", (username, email.lower(), password))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(error.sqlite_errorcode)
        print(error.sqlite_errorname)
        return False
    finally:
        cur.close()
        conn.close()


def validate_login(username, password):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT password FROM user WHERE username = ?", (username,))
        password_fetched = cur.fetchall()

        if ph.verify_password(password, password_fetched):
            return True
        else:
            return False
    except sqlite3.Error as error:
        print(error.sqlite_errorcode)
        print(error.sqlite_errorname)
        return False
    finally:
        cur.close()
        conn.close()

