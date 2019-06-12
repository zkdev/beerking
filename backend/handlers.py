from . import validate, sql, elo, log
from .enums import Username, Mail, Create, Login


def create_user(conn, userid, username, mail, passwd):
    c = conn.cursor()
    username_status = validate.check_username(conn, username)
    if mail is None or mail == "":
        mail = ""
        mail_status = Mail.FINE
    else:
        mail_status = validate.check_mail(mail)

    if username_status is Username.FINE and mail_status is Mail.FINE:
        log.info('creating user \"' + str(username) + '\"')
        sql.create_user(c, userid, username, mail, passwd, elo.initial_elo())
        return Create.ERFOLGREICH
    else:
        if username_status is Username.TOO_SHORT:
            return Create.NUTZERNAME_ERFUELLT_BEDINGUNGEN_NICHT
        elif username_status is Username.EXISTS:
            return Create.NUTZERNAME_EXISTIERT_BEREITS
        else:
            return Create.MAIL_EXISTIERT_NICHT


def login(conn, username, passwd):
    c = conn.cursor()
    username_status = validate.check_username(conn, username)
    if username_status is Username.EXISTS:
        r = sql.login(c, username, passwd)
        if r is None:
            return Login.PASSWD_WRONG
        else:
            return Login.SUCCESSFUL
    else:
        return Login.USERNAME_NOT_FOUND


def get_profile(r, conn, username, passwd):
    if r is Login.SUCCESSFUL:
        return sql.get_profile(conn, username, passwd)
