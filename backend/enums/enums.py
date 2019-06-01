from enum import Enum


class Username(Enum):
    FINE = 0
    EXISTS = 1
    TOO_SHORT = 2


class Mail(Enum):
    FINE = 0
    NOT_EXISTING = 1
