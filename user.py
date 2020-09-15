import database


class UserCondition:
    BEGIN = 0
    SETTINGS = 1
    SETTINGS_NAME = 2
    SETTINGS_AGE = 3
    SETTINGS_INFO = 4
    SETTINGS_PHOTO = 5
    MAIN_MENU = 6
    SEARCHING_PARTNER = 7
    SEARCHING_CHAT = 8
    CHATTING = 9


class User:
    def __init__(self, id: int, condition: int = UserCondition.BEGIN):
        self.id: int = id

        self.name:      str = None
        self.age:       int = None
        self.info:      str = None
        self.photo:     str = None
        self.condition: int = condition
        self.proposed_partner: User = None
        self.proposed_partner_is_fan: bool = None

        self.fanbase:   set = set()  # set<int> ids of users that liked this

    @classmethod
    def create_from_db_row(cls, id: int, name: str, age: int, info: str, photo: str, fanbase: str):
        user = User(id, UserCondition.MAIN_MENU)

        user.name = name
        user.age = age
        user.info = info
        user.photo = photo

        user.fanbase = set([int(id) for id in fanbase.split()])

        return user

    def set_proposed_partner(self, user, is_fan: bool):
        self.proposed_partner: User = user
        self.proposed_partner_is_fan: bool = is_fan

    def is_fan_of(self, user):
        return self.id in user.fanbase

    def update_fanbase(self):
        database.update_fanbase(self.id, self.fanbase)

    def discard_fanbase(self, fan_id: int):
        self.fanbase.discard(fan_id)

    def discard_update_fanbase(self, fan_id: int):
        self.discard_fanbase(fan_id)
        self.update_fanbase()

    def expand_fanbase(self, fan_id: int):
        self.fanbase.add(fan_id)

    def expand_update_fanbase(self, fan_id: int):
        self.expand_fanbase(fan_id)
        self.update_fanbase()

    def pop_fanbase(self) -> int:
        if len(self.fanbase) > 0:
            return self.fanbase.pop()
        return None

    def pop_update_fanbase(self) -> int:
        id = self.pop_fanbase()
        if id is not None:
            self.update_fanbase()
        return id

    def get_profile_info(self) -> str:
        return f"{self.name}, {self.age}:\n" \
               f"\"{self.info}\""

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __le__(self, other):
        return self.id <= other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __str__(self):
        return f"User({self.id}, {self.fanbase})"
