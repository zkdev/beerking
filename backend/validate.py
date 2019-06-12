from validate_email import validate_email
from .enums import Username, Mail
from . import sql


def check_mail(mail):
    if validate_email(str(mail), verify=True):
        return Mail.FINE
    else:
        return Mail.NOT_EXISTING


def check_username(conn, username):
    if not str(username).__len__() > 5:
        return Username.TOO_SHORT
    if not is_unique(conn, 'username', username):
        return Username.EXISTS
    return Username.FINE


def is_unique(conn, key, value):
    r = sql.is_unique(conn, key, value).fetchone()
    if r is None:
        return True
    else:
        return False
