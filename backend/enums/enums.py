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
    SUCCESSFUL = 0
    USERNAME_NOT_UNIQUE = 1
    USERNAME_DOESNT_MATCH_REQUIREMENTS = 2
    MAIL_NOT_EXISTING = 3
