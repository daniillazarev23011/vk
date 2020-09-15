from user import User
from bisect import insort


class UsersList:
    def __init__(self, users=[]):
        self._users = []
        for user in users:
            self.add(user)

    def _get_index_by_id(self, id: int):
        low = 0
        high = len(self._users) - 1
        while low <= high:
            mid = (high + low) // 2
            if self._users[mid].id < id:
                low = mid + 1
            elif self._users[mid].id > id:
                high = mid - 1
            else:
                return mid
        return -1

    def get_by_id(self, id: int) -> User:
        i = self._get_index_by_id(id)
        if i != -1:
            return self._users[i]
        return None

    def pop_by_id(self, id: int) -> User:
        i = self._get_index_by_id(id)
        if i != -1:
            return self._users.pop(i)
        return None

    def pop(self, user: User = None) -> User:
        if user is not None:
            return self.pop_by_id(user.id)
        return self._users.pop()

    def add(self, user: User):
        insort(self._users, user)

    def get_list(self):
        return self._users

    def __isub__(self, other: User):
        return self.pop_by_id(other.id)

    def __iadd__(self, other: User):
        insort(self._users, other)

    def __contains__(self, user: User):
        return self._get_index_by_id(user.id) != -1

    def __getitem__(self, i):
        return self._users[i]

    def __len__(self):
        return len(self._users)
