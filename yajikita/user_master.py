from datetime import date
import sqlite3

user_db = 'yajikita.sqlite'

def initialize():
    connection = sqlite3.connect(user_db)
    cursor = connection.cursor()
    print("init...")
    try:
        for drop_table_name in ('USERS', 'STEPS', 'RACES', 'RACE_MEMBERS'):
            cursor.execute('DROP TABLE IF EXISTS {}'.format(drop_table_name))
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
            steps INTEGER,
            PRIMARY KEY (date, user_id)
        )''')
        cursor.execute('''
        CREATE TABLE RACES (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL
        )''')
        cursor.execute('''
        CREATE TABLE RACE_MEMBERS (
            race_id INTEGER,
            user_id TEXT,
            PRIMARY KEY (race_id, user_id)
        )''')
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
    connection.commit()
    connection.close()


def update_user(uname, access_token="", refresh_token="", displayName="", avatar=""):
    ret = {}
    with sqlite3.connect(user_db) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, displayName, avatar FROM USERS WHERE id=?', (uname,))
        data = cursor.fetchone()
        if not data:
            ret = {'user_id': uname, 'name': displayName, 'avatar': avatar}
            cursor.execute(
                "INSERT INTO USERS VALUES (?, ?, ?, ?, ?)",
                (uname, access_token, refresh_token, displayName, avatar))
        else:
            ret = {'user_id': data[0], 'name': data[1], 'avatar': data[2]}
            if access_token == "":
                ret['name'] = displayName
                ret['avatar'] = avatar
                cursor.execute(
                    "UPDATE USERS SET displayName=?, avatar=? WHERE id=?",
                    (displayName, avatar, uname))
            else:
                cursor.execute(
                    "UPDATE USERS SET access_token=?, refresh_token=? WHERE id=?",
                    (access_token,refresh_token, uname))
        conn.commit()
    return ret


def get_dashboard_info(user_id):
    # TODO: ISUCON!
    ret = {'user_id': user_id, 'users': {}, 'races': []}
    n_running = 0
    user_set = set()
    today = date.today()
    with sqlite3.connect(user_db) as conn:
        cursor = conn.cursor()

        # ユーザが属するレースを取得
        e = cursor.execute('''
            SELECT
                RACES.id,
                RACES.name,
                RACES.start,
                RACES.end
            FROM
                RACES,
                RACE_MEMBERS
            WHERE
                RACES.id=RACE_MEMBERS.race_id AND
                RACE_MEMBERS.user_id=?
        ''', (user_id,))
        races = [{
            'id': r[0], 'name': r[1], 'start': r[2], 'end': r[3]
        } for r in e]
        ret['races'] = races
        for r in races:
            s = date.fromisoformat(r['start'])
            e = date.fromisoformat(r['end'])
            if s <= today and today <= e:
                n_running += 1

        # TODO: 開催終了したレースを取り除く

        # レースごとにその期間のユーザごとの歩数を集計する
        for race in races:
            e = cursor.execute('''
                SELECT
                    RACE_MEMBERS.user_id,
                    SUM(STEPS.steps)
                FROM
                    RACE_MEMBERS,
                    STEPS
                WHERE
                    RACE_MEMBERS.user_id=STEPS.user_id AND
                    RACE_MEMBERS.race_id=? AND
                    STEPS.date >= ? AND
                    STEPS.date <= ?
                GROUP BY
                    RACE_MEMBERS.user_id
            ''', (race['id'], race['start'], race['end']))
            race['members'] = [{
                'user_id': r[0], 'steps': r[1]
            } for r in e]
            race['members'].sort(key=lambda x: x['steps'], reverse=True)
            user_set |= set([x['user_id'] for x in race['members']])

        # ユーザの情報を取得する
        e = cursor.execute(
            'SELECT id, displayName, avatar FROM USERS WHERE id in ({})'.format(
                ('?,' * len(user_set))[:-1]), tuple(user_set))
        ret['users'] = {r[0]: {'name': r[1], 'avatar': r[2]} for r in e}

        if user_id in ret['users']:
            ret['name'] = ret['users'][user_id]['name']
            ret['avatar'] = ret['users'][user_id]['avatar']
        else:
            # レースが1つもない場合
            u = cursor.execute('SELECT displayName, avatar FROM USERS WHERE id=?', (user_id,)).fetchone()
            ret['name'] = u[0]
            ret['avatar'] = u[1]
        ret['n_races'] = {
            'running': n_running
        }
    return ret
