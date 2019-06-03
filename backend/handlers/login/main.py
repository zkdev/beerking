from ...validate.check_username import main as check_username
from ...enums.enums import Username, Login
from ...connection.sql.login import main as login


def main(conn, username, passwd):
    c = conn.cursor()
    username_status = check_username(conn, username)
    if username_status is Username.EXISTS:
        r = login(c, username, passwd)
        if r is None:
            return Login.PASSWD_WRONG
        else:
            return Login.SUCCESSFUL
    else:
        return Login.USERNAME_NOT_FOUND
