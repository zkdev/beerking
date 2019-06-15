from . import sql, generator, elo
from .enums import Match, Mode


def start_1v1(conn, host, enemy, winner):
    try:
        matchid = generator.create_uuid(conn)
        sql.start_1v1(conn, matchid, host, enemy, winner)
        return Match.STARTED
    except:
        return Match.NOT_STARTED


def start_2v2(conn, host, friend, enemy1, enemy2, winner):
    try:
        matchid = generator.create_uuid(conn)
        sql.start_2v2(conn, matchid, host, friend, enemy1, enemy2, winner)
        return Match.STARTED
    except:
        return Match.NOT_STARTED


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


def update_elo(conn, matchid, mode, winner):
    if mode is Mode.SOLO:
        participants = sql.get_match_participants(conn, matchid).fetchall()
        host = participants[0][0]
        enemy1 = participants[0][2]
        host_elo_old = sql.get_elo(conn, host).fetchone()[0]
        enemy1_elo_old = sql.get_elo(conn, enemy1).fetchone()[0]
        if int(winner) == 0:
            # winner = host
            elo_new = elo.rate_1v1(host_elo_old, enemy1_elo_old)
            host_elo_new = int(elo_new[0] + 1)
            enemy1_elo_new = int(elo_new[1])
        else:
            # winner = enemy
            elo_new = elo.rate_1v1(enemy1_elo_old, host_elo_old)
            enemy1_elo_new = int(elo_new[0] + 1)
            host_elo_new = int(elo_new[1])
        sql.update_elo(conn, host, host_elo_new)
        sql.update_elo(conn, enemy1, enemy1_elo_new)
        sql.update_elo_history(conn, matchid, host_elo_old, 0, enemy1_elo_old, 0, host_elo_new, 0, enemy1_elo_new, 0)
    elif mode is Mode.DUO:
        participants = sql.get_match_participants(conn, matchid).fetchall()
        host, friend, enemy1, enemy2 = participants[0]
        host_elo_old = sql.get_elo(conn, host).fetchone()[0]
        friend_elo_old = sql.get_elo(conn, friend).fetchone()[0]
        enemy1_elo_old = sql.get_elo(conn, enemy1).fetchone()[0]
        enemy2_elo_old = sql.get_elo(conn, enemy2).fetchone()[0]
        if int(winner) == 0:
            # winner = team_host
            elo_new = elo.rate_2v2(host_elo_old, friend_elo_old, enemy1_elo_old, enemy2_elo_old)
            host_elo_new = int(elo.rate_1v1(host_elo_old, elo_new[1])[0] + 1)
            friend_elo_new = int(elo.rate_1v1(friend_elo_old, elo_new[1])[0] + 1)
            enemy1_elo_new = int(elo.rate_1v1(elo_new[0], enemy1_elo_old)[1])
            enemy2_elo_new = int(elo.rate_1v1(elo_new[0], enemy2_elo_old)[1])
        else:
            # winner = team_enemy
            elo_new = elo.rate_2v2(enemy1_elo_old, enemy2_elo_old, host_elo_old, friend_elo_old)
            host_elo_new = int(elo.rate_1v1(elo_new[0], host_elo_old)[1])
            friend_elo_new = int(elo.rate_1v1(elo_new[0], friend_elo_old)[1])
            enemy1_elo_new = int(elo.rate_1v1(enemy1_elo_old, elo_new[1])[0] + 1)
            enemy2_elo_new = int(elo.rate_1v1(enemy2_elo_old, elo_new[1])[0] + 1)
        sql.update_elo(conn, host, host_elo_new)
        sql.update_elo(conn, friend, friend_elo_new)
        sql.update_elo(conn, enemy1, enemy1_elo_new)
        sql.update_elo(conn, enemy2, enemy2_elo_new)
        sql.update_elo_history(conn, matchid, host_elo_old, friend_elo_old, enemy1_elo_old, enemy2_elo_old, host_elo_new, friend_elo_new, enemy1_elo_new, enemy2_elo_new)
