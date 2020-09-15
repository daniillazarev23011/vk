import random
import database
from user import User
from users_list import UsersList

new_users: UsersList = None
registered_users: UsersList = None
searching_chat_users: UsersList = None


def initialize():
    global new_users, registered_users, searching_chat_users
    new_users = UsersList()
    registered_users = UsersList(list(database.all_users()))
    searching_chat_users = UsersList()


def get_user_by_id(id: int) -> User:
    user = get_registered_user_by_id(id)
    if user is None:
        # try get from new users
        user = new_users.get_by_id(id)
        if user is None:
            # create new user
            user = User(id)
            new_users.add(user)

    return user


def get_registered_user_by_id(id: int) -> User:
    global registered_users
    # try get from online
    user = registered_users.get_by_id(id)
    if user is None:
        # try get from db
        user = database.get_user_by_id(id)
        if user is not None:
            registered_users.add(user)
    return user


def register_user(user: User) -> bool:
    database.insert_or_update(user)
    return True


def get_fan_of(user: User) -> User:
    while (fan_id := user.pop_update_fanbase()) is not None:
        fan = get_registered_user_by_id(fan_id)
        if fan is not None:
            return fan
    return None


def get_random_partner(user: User) -> User:
    global registered_users

    partner = None
    i = 20
    while i > 0:
        # try choice partner 10 times
        partner = random.choice(registered_users.get_list())
        if partner != user:
            break
        i -= 1

    if partner == user:
        return None
    return partner


def get_chat(user: User) -> User:
    global searching_chat_users

    if user not in searching_chat_users:
        if len(searching_chat_users) > 0:
            return searching_chat_users.pop()
        else:
            searching_chat_users.add(user)
            return None
    else:
        return None
