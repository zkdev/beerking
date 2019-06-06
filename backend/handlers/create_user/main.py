from ...validate.check_username import main as check_username
from ...validate.check_mail import main as check_mail
from ...enums.enums import Username, Mail, Create
from ...connection.sql.create_user import main as create_user


def main(conn, userid, username, mail, passwd):
    c = conn.cursor()
    username_status = check_username(conn, username)
    mail_status = check_mail(mail)

    if username_status is Username.FINE and mail_status is Mail.FINE:
        create_user(c, userid, username, mail, passwd)
        return Create.SUCCESSFUL
    else:
        if username_status is Username.TOO_SHORT:
            return Create.USERNAME_DOESNT_MATCH_REQUIREMENTS
        elif username_status is Username.EXISTS:
            return Create.USERNAME_NOT_UNIQUE
        else:
            return Create.MAIL_NOT_EXISTING
