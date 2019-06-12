from enum import Enum


class Username(Enum):
    FINE = 0
    EXISTS = 1
    TOO_SHORT = 2


class Mail(Enum):
    FINE = 0
    NOT_EXISTING = 1


class Login(Enum):
    SUCCESSFUL = 0
    PASSWD_WRONG = 1
    USERNAME_NOT_FOUND = 2


class Create(Enum):

    # not translated in the frontend so it has to match with the german language

    ERFOLGREICH = 0
    NUTZERNAME_EXISTIERT_BEREITS = 1
    NUTZERNAME_ERFUELLT_BEDINGUNGEN_NICHT = 2
    MAIL_EXISTIERT_NICHT = 3


class Match(Enum):
    FINE = 0
    RECEIVED = 1
    CONFIRMED = 2


class Profile(Enum):
    SUCCESSFUL = 0
    REJECTED = 1
    UPDATED = 3


class Leaderboard(Enum):
    FINE = 0


class Mode(Enum):
    SOLO = 0
    DUO = 1


class History(Enum):
    FINE = 0
    ERROR = 1


class Id(Enum):
    EXISTS = 0
    DOESNT_EXIST = 1


class Error(Enum):
    ERROR = 0
