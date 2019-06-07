from .connection.sql.start_1v1 import main as sql_1v1
from .connection.sql.start_2v2 import main as sql_2v2
from .connection.sql.get_pending_matches import main as sql_pending_matches
from .connection.sql.get_match import main as sql_get_match
from .connection.sql.confirm_match import main as sql_confirm_match
from .enums.enums import Match


def match_1v1(conn, host, enemy, winner):
    sql_1v1(conn, host, enemy, winner)
    return Match.FINE


def match_2v2(conn, host, friend, enemy1, enemy2, winner):
    sql_2v2(conn, host, friend, enemy1, enemy2, winner)
    return Match.FINE


def get_pending_matches(conn, userid):
    rs = sql_pending_matches(conn, userid).fetchall()
    arr = []
    for entry in rs:
        matchid = entry[0]
        winner = entry[2]
        datetime = entry[3]
        hostname = entry[4]
        arr.append({"matchid": matchid, "hostname": hostname, "winner": winner, "datetime": datetime})
    return arr


def confirm_match(conn, matchid):
    m = sql_get_match(conn, matchid).fetchall()
    sql_confirm_match(conn, m[0][0], m[0][1], m[0][2], m[0][3], m[0][4], m[0][5], m[0][6])
    return Match.CONFIRMED
