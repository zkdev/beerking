from . import sql, log, generator, elo
from .enums import Match, Mode


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
    if m[0][2] is None:
        update_elo(conn, matchid, Mode.SOLO, m[0][5])
    else:
        update_elo(conn, matchid, Mode.DUO, m[0][5])
    return Match.CONFIRMED


def update_elo(conn, matchid, mode, winner):
    if mode is Mode.SOLO:
        participants = sql.get_match_participants(conn, matchid).fetchall()
        host = participants[0][0]
        enemy1 = participants[0][2]
        host_elo = sql.get_elo(conn, host).fetchone()[0]
        enemy1_elo = sql.get_elo(conn, enemy1).fetchone()[0]
        if int(winner) == 0:
            elo_new = elo.rate_1v1(host_elo, enemy1_elo)
            host_new = elo_new[0]
            enemy1_new = elo_new[1]
        else:
            elo_new = elo.rate_1v1(enemy1_elo, host_elo)
            enemy1_new = elo_new[0]
            host_new = elo_new[1]
        sql.update_elo(conn, host, host_new)
        sql.update_elo(conn, enemy1, enemy1_new)
    elif mode is Mode.DUO:
        participants = sql.get_match_participants(conn, matchid).fetchall()
        host = participants[0][0]
        friend = participants[0][1]
        enemy1 = participants[0][2]
        enemy2 = participants[0][3]
        host_elo = sql.get_elo(conn, host).fetchone()[0]
        friend_elo = sql.get_elo(conn, friend).fetchone()[0]
        enemy1_elo = sql.get_elo(conn, enemy1).fetchone()[0]
        enemy2_elo = sql.get_elo(conn, enemy2).fetchone()[0]
        if int(winner) == 0:
            elo_new = elo.rate_2v2(host_elo, friend_elo, enemy1_elo, enemy2_elo)
            host_new = elo.rate_1v1(host_elo, elo_new[1])[0]
            friend_new = elo.rate_1v1(friend_elo, elo_new[1])[0]
            enemy1_new = elo.rate_1v1(elo_new[0], enemy1_elo)[1]
            enemy2_new = elo.rate_1v1(elo_new[0], enemy2_elo)[1]
        else:
            elo_new = elo.rate_2v2(enemy1_elo, enemy2_elo, host_elo, friend_elo)
            host_new = elo.rate_1v1(elo_new[0], host_elo)[1]
            friend_new = elo.rate_1v1(elo_new[0], friend_elo)[1]
            enemy1_new = elo.rate_1v1(enemy1_elo, elo_new[1])[0]
            enemy2_new = elo.rate_1v1(enemy2_elo, elo_new[1])[0]
        sql.update_elo(conn, host, host_new)
        sql.update_elo(conn, friend, friend_new)
        sql.update_elo(conn, enemy1, enemy1_new)
        sql.update_elo(conn, enemy2, enemy2_new)
    else:
        log.error('match mode not found')
