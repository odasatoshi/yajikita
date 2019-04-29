import sqlite3

user_db = 'user_master.sqlite'

def initialize():
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    print("init...")
    try:
        cursor.execute("DROP TABLE IF EXISTS USER")
        cursor.execute(
    "CREATE TABLE IF NOT EXISTS USER (userid TEXT PRIMARY KEY, access_token TEXT, refresh_token TEXT)")
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()
    connection.close()

def update_user(uname, access_token, refresh_token=None):
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    try:
        cursor.execute(
    "INSERT INTO USER VALUES (?, ? , ?)",  (uname,access_token,refresh_token))
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()
    connection.close()

