from ...connection.sql.get_profile import main as get_profile
from ...enums.enums import Login, Profile


def main(r, conn, username, passwd):
    if r is Login.SUCCESSFUL:
        return get_profile(conn, username, passwd)
