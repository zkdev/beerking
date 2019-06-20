from enum import Enum


class User(Enum):
    WILL_CREATE = 0
    WONT_CREATE = 1
    CREATED = 2
    NOT_CREATED = 3
    MAIL_UPDATED = 4
    MAIL_UPDATE_FAILED = 5
    ID_EXISTS = 6
    ID_DOESNT_EXIST = 7
    BANNED = 8


class Mail(Enum):
    UPDATED = 0
    UPDATE_FAILED = 1


class Auth(Enum):
    SUCCESSFUL = 0
    FAILED = 1


class Match(Enum):
    STARTED = 0
    NOT_STARTED = 1
    RECEIVED = 2
    CONFIRMED = 3


class Profile(Enum):
    SUCCESSFUL = 0
    REJECTED = 1
    UPDATED = 3


class Leaderboard(Enum):
    RETRIEVED = 0
    NOT_RETRIEVED = 1


class Mode(Enum):
    SOLO = 0
    DUO = 1


class History(Enum):
    RETRIEVED = 0


class Friends(Enum):
    RETRIEVED = 0
    ADDED = 1
    REMOVED = 2
    NOT_ADDED = 3


class Error(Enum):
    VERSION_OUTDATED = 0
    SECURITY_INCIDENT = 1


class Reason(Enum):
    USERNAME_NOT_UNIQUE = 0
    USERNAME_TOO_SHORT = 1
    MAIL_DOESNT_EXIST = 2
    FRIEND_DOESNT_EXIST = 3
    FRIENDS_ALREADY = 4
    SAME_AS_USER = 5


class UniqueMode(Enum):
    USER_ID = 0
    USERNAME = 1
    MATCH_ID = 2
