import sqlite3

user_db = 'user_master.sqlite'

def initialize():
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    print("init...")
    try:
        cursor.execute("DROP TABLE IF EXISTS STEPS")
        cursor.execute('''
        CREATE TABLE USERS (
            id TEXT PRIMARY KEY,
            access_token TEXT,
            refresh_token TEXT,
            displayName TEXT,
            avatar TEXT
        )''')
        cursor.execute('''
        CREATE TABLE STEPS (
            date TEXT,
            user_id TEXT,
            is_partial INTEGER,
            PRIMARY KEY (date, user_id)
        )''')
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

def list_users():
    with sqlite3.connect(user_db) as conn:
        cursor = conn.cursor()
        return [
            {'id': row[0], 'access_token': row[1], 'refresh_token': row[2]}
            for row in cursor.execute(
                    'SELECT id, access_token, refresh_token FROM USERS')]
