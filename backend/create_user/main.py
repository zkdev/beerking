from validate.check_username import main as check_username
from validate.check_mail import main as check_mail
from enums.enums import Username, Mail
from connection.sql.create_user import main as create_user


def main(conn, uuid, username, mail, passwd):
    c = conn.cursor()
    username_status = check_username(conn, username)
    mail_status = check_mail(mail)

    if username_status is Username.FINE and mail_status is Mail.FINE:
        create_user(c, uuid, username, mail, passwd)
        return 'user created.<br>uuid: ' + str(uuid) + '<br>username: ' + str(username) + '<br>email: ' + str(mail)
    else:
        if username_status is not Username.FINE:
            return 'creating user failed<br>' + str(username_status)
        else:
            return 'creating user failed<br>' + str(mail_status)