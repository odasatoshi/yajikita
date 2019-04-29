import sqlite3

user_db = 'user_master.sqlite'

def initialize():
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    print("init...")
    try:
        cursor.execute("DROP TABLE IF EXISTS USER")
        cursor.execute(
    "CREATE TABLE IF NOT EXISTS USER (userid TEXT PRIMARY KEY, access_token TEXT, refresh_token TEXT, displayName TEXT, avatar TEXT)")
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()
    connection.close()

def update_user(uname, access_token="", refresh_token="", displayName="", avatar=""):
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM USER WHERE userid=?', (uname,))
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.execute(
            "INSERT INTO USER VALUES (?, ?, ?, ?, ?)",  (uname,access_token,refresh_token, displayName, avatar))
        else:
            if access_token == "":
                cursor.execute(
                "UPDATE USER SET displayName=?, avatar=? WHERE userid=?",
                  (displayName, avatar, uname))
            else:
                cursor.execute(
                "UPDATE USER SET access_token=?, refresh_token=? WHERE userid=?",
                  (access_token,refresh_token, uname))

    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()
    connection.close()

def list_user():
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    try:
        result = cursor.execute(
    "SELECT userid, access_token FROM USER")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()
    connection.close()
    return data

    

    