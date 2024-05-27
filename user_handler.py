# import sqlite3 for database interaction
import sqlite3


# def singleton(cls):
#     instance = None
#
#     def getinstance():
#         nonlocal instance
#         if instance is None:
#             instance = cls()
#         return instance
#     return getinstance()


# database connection method
def db__connect():
    conn = None
    try:
        conn = sqlite3.connect("user_database.db")
    except sqlite3.Error as error:
        print(error.sqlite_errorcode)
        print(error.sqlite_errorname)
    return conn


# Current user class which holds the current user's data
# @singleton
class CurrentUser:
    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

