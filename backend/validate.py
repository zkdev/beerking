from validate_email import validate_email

import sql
import config
from enums import UniqueMode


def mail_is_fine(mail):
    if validate_email(str(mail), verify=True):
        return True
    else:
        return False


def username_is_fine(conn, username):
    if str(username).__len__() > 2 and is_unique(conn, UniqueMode.USERNAME, username):
        return True
    else:
        return False


def is_unique(conn, mode, value):
    r = sql.is_unique(conn, mode, value).fetchone()
    if r is None:
        return True
    else:
        return False


def is_correct_version(device_version):
    print("device version:" + str(device_version), flush=True)
    if int(device_version) >= int(config.app_version):
        return True
    else:
        return False


def catch_empty_auth(username, passwd):
    if str(username) is "" and str(passwd) is "":
        return True
    else:
        return False


def catch_empty_mail(mail):
    if mail is None or mail == "":
        return True
    else:
        return False
