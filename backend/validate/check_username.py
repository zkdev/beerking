from validate.is_unique import main as is_unique
from enums.enums import Username
from logger import log


def main(conn, username):
    if not str(username).__len__() > 5:
        log.info('\"' + str(username) + '\" as username rejected (too short)')
        return Username.TOO_SHORT
    if not is_unique(conn, 'username', username):
        log.info('\"' + str(username) + '\" as username rejected (exists)')
        return Username.EXISTS
    log.info('\"' + str(username) + '\" as username accepted')
    return Username.FINE
