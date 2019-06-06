from .connection.sql.start_1v1 import main as sql_start_1v1
from .connection.sql.start_2v2 import main as sql_start_2v2
from .enums.enums import Match


def start_1v1(conn, host, enemy):
    sql_start_1v1(conn, host, enemy)
    return Match.PENDING


def start_2v2(conn, host, friend, enemy1, enemy2):
    sql_start_2v2(conn, host, friend, enemy1, enemy2)
    return Match.PENDING
