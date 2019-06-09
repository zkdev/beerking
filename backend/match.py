from . import sql, log, generator
from .enums import Match


def start_1v1(conn, host, enemy, winner):
    matchid = generator.create_uuid(conn)
    sql.start_1v1(conn, matchid, host, enemy, winner)
    host = sql.get_username(conn, host).fetchone()[0]
    enemy = sql.get_username(conn, enemy).fetchone()[0]
    if int(winner) == 0:
        winner = host
    elif int(winner) == 1:
        winner = enemy
    log.info('starting 1v1 match (' + host + ' vs. ' + enemy + ' ; ' + winner + ' wins)')
    return Match.FINE


def start_2v2(conn, host, friend, enemy1, enemy2, winner):
    matchid = generator.create_uuid(conn)
    sql.start_2v2(conn, matchid, host, friend, enemy1, enemy2, winner)
    host = sql.get_username(conn, host).fetchone()[0]
    friend = sql.get_username(conn, friend).fetchone()[0]
    enemy1 = sql.get_username(conn, enemy1).fetchone()[0]
    enemy2 = sql.get_username(conn, enemy2).fetchone()[0]
    if int(winner) == 0:
        winner = host + ' and ' + friend
    elif int(winner) == 1:
        winner = enemy1 + ',' + enemy2
    log.info('starting 2v2 match (' + host + ' and ' + friend + ' vs. ' + enemy1 + ' and ' + enemy2 + ' ; ' + winner + ' win)')
    return Match.FINE


def get_pending_matches(conn, userid):
    rs = sql.get_pending_matches(conn, userid).fetchall()
    arr = []
    for entry in rs:
        matchid = entry[0]
        winner = entry[2]
        datetime = entry[3]
        hostname = entry[4]
        arr.append({"matchid": matchid, "hostname": hostname, "winner": winner, "datetime": datetime})
    return arr


def confirm_match(conn, matchid):
    m = sql.get_match(conn, matchid).fetchall()
    sql.confirm_match(conn, m[0][0], m[0][1], m[0][2], m[0][3], m[0][4], m[0][5], m[0][6])
    return Match.CONFIRMED
