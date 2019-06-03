from ..enums.enums import Username
from .is_unique import main as is_unique


def main(conn, username):
    if not str(username).__len__() > 5:
        return Username.TOO_SHORT
    if not is_unique(conn, 'username', username):
        return Username.EXISTS
    return Username.FINE
