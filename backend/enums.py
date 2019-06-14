from enum import Enum


class User(Enum):
    WILL_CREATE = 0
    WONT_CREATE = 1
    CREATED = 2
    NOT_CREATED = 3
    MAIL_UPDATED = 4
    MAIL_UPDATE_FAILED = 5


class Mail(Enum):
    UPDATED = 0
    UPDATE_FAILED = 1


class Login(Enum):
    SUCCESSFUL = 0
    PASSWD_WRONG = 1
    USERNAME_NOT_FOUND = 2
    FAILED = 3


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


class Id(Enum):
    EXISTS = 0
    DOESNT_EXIST = 1


class Error(Enum):
    ERROR = 0


class Friends(Enum):
    FINE = 0
    ADDED = 1
    REMOVED = 2


class Version(Enum):
    OUTDATED = 0
