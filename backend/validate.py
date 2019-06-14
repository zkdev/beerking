from validate_email import validate_email
from . import sql


version = 104


def check_mail(mail):
    if validate_email(str(mail), verify=True):
        return True
    else:
        return False


def username_is_fine(conn, username):
    if str(username).__len__() > 2 and is_unique(conn, 'username', username):
        return True
    else:
        return False


def is_unique(conn, key, value):
    r = sql.is_unique(conn, key, value).fetchone()
    if r is None:
        return True
    else:
        return False


def is_correct_version(device_version):
    if int(device_version) == int(version):
        return True
    else:
        return False
