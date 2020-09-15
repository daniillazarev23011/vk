import sqlite3
from user import User
from utils import to_string


DATABASE_FILE_NAME = "database"
USERS_TABLE = "users"

database: sqlite3.Connection = None
cursor: sqlite3.Cursor = None


def open():
    global database, cursor
    database = sqlite3.connect(DATABASE_FILE_NAME)
    cursor = database.cursor()

    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {USERS_TABLE} ("
        f"id INTEGER PRIMARY KEY, "
        f"name TEXT, "
        f"age INTEGER, "
        f"info TEXT, "
        f"photo TEXT, "
        f"fanbase TEXT);"
    )
    database.commit()


def close():
    global database
    database.commit()
    database.close()


def insert_user(user: User):
    global database, cursor
    cursor.execute(
        f"INSERT INTO {USERS_TABLE} "
        f"VALUES ({user.id}, '{user.name}', {user.age}, "
        f"'{user.info}', '{user.photo}', "
        f"'{to_string(user.fanbase)}');"
    )
    database.commit()


def update_user(user: User):
    global database, cursor
    cursor.execute(
        f"UPDATE {USERS_TABLE} "
        f"SET name =       '{user.name}', "
        f"    age =         {user.age}, "
        f"    info =       '{user.info}', "
        f"    photo =      '{user.photo}', "
        f"    fanbase =    '{to_string(user.fanbase)}', "
        f"WHERE vk_id =     {user.id};"
    )
    database.commit()


def update_fanbase(user_id: int, fanbase: set):
    global database, cursor
    cursor.execute(
        f"UPDATE {USERS_TABLE} "
        f"SET fanbase = '{to_string(fanbase)}' "
        f"WHERE id = {user_id};"
    )
    database.commit()


def insert_or_update(user: User):
    global database, cursor
    cursor.execute(
        f"INSERT OR REPLACE INTO {USERS_TABLE} "
        f"VALUES ({user.id}, '{user.name}', {user.age}, "
        f"'{user.info}', '{user.photo}', '{to_string(user.fanbase)}');"
    )
    database.commit()


def delete_user(id: int):
    global database, cursor
    cursor.execute(
        f"DELETE FROM {USERS_TABLE} WHERE id = {id}"
    )
    database.commit()


def get_user_by_id(id: int) -> User:
    global cursor
    cursor.execute(
        f"SELECT * FROM {USERS_TABLE} WHERE id = {id}"
    )
    users = cursor.fetchall()
    if len(users) == 1:
        return User.create_from_db_row(*users[0])
    return None


def all_users():
    global cursor
    for row in cursor.execute(f"SELECT * FROM {USERS_TABLE}"):
        yield User.create_from_db_row(*row)
