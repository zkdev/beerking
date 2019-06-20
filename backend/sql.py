import datetime


from . import log
from .enums import UniqueMode


def get_match(conn, matchid):
    c = conn.cursor()
    return c.execute("""SELECT * FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))


def is_unique(conn, mode, value):
    c = conn.cursor()
    if mode is UniqueMode.USER_ID:
        sql = """SELECT 1 FROM Users WHERE userid = ? COLLATE NOCASE;"""
    elif mode is UniqueMode.USERNAME:
        sql = """SELECT 1 FROM Users WHERE username = ? COLLATE NOCASE;"""
    elif mode is UniqueMode.MATCH_ID:
        sql = """SELECT 1 FROM Matches WHERE matchid = ? COLLATE NOCASE;"""
    return c.execute(sql, (str(value),))


def leaderboard(conn):
    c = conn.cursor()
    return c.execute("""SELECT userid, username, elo FROM Users ORDER BY elo DESC;""")


def login(c, username, passwd):
    return c.execute("""SELECT 1 FROM users WHERE username = ? and passwd = ?;""", (str(username), str(passwd))).fetchone()


def remove_pending_match(conn, matchid):
    c = conn.cursor()
    c.execute("""DELETE FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))


def start_1v1(conn, matchid, host, enemy, winner, date):
    c = conn.cursor()
    return c.execute("""INSERT INTO PendingMatches(matchid, host, enemy1, winner, datetime) 
        VALUES (?,?,?,?,?);""", (str(matchid), str(host), str(enemy), str(winner), str(date)))


def start_2v2(conn, matchid, host, friend, enemy1, enemy2, winner, date):
    c = conn.cursor()
    return c.execute("""INSERT INTO PendingMatches(matchid, host, friend, enemy1, enemy2, winner, datetime) 
        VALUES (?,?,?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2),
                                     str(winner), str(date)))


def get_profile(conn, username, passwd):
    c = conn.cursor()
    return c.execute("""SELECT userid, mail FROM Users WHERE username = ? AND passwd = ?;""", (str(username), str(passwd)))


def get_username(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT username FROM Users WHERE userid = ?;""", (str(userid),))


def get_pending_matches(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT matchid, host, winner, datetime, username FROM PendingMatches, Users WHERE Users.userid = host AND (enemy1 = ? OR enemy2 = ?);""", (str(userid), str(userid)))


def create_user(conn, userid, username, mail, passwd, elo, create_date):
    c = conn.cursor()
    c.execute("""INSERT INTO users(userid, username, mail, passwd, elo, create_date) 
        VALUES (?,?,?,?,?);""", (str(userid), str(username), str(mail), str(passwd), int(elo), str(create_date)))


def confirm_match(conn, matchid, host, friend, enemy1, enemy2, winner, date_data):
    c = conn.cursor()
    c.execute("""INSERT INTO Matches(matchid, host, friend, enemy1, enemy2, winner, datetime) 
        VALUES (?,?,?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2), int(winner), str(date_data)))


def update_elo(conn, userid, elo):
    c = conn.cursor()
    c.execute("""UPDATE Users SET elo = ? WHERE userid = ?;""", (int(elo), str(userid),))


def get_match_participants(conn, matchid):
    c = conn.cursor()
    return c.execute("""SELECT host, friend, enemy1, enemy2 FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))


def get_elo(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT elo FROM Users WHERE userid = ?;""", (str(userid),))


def get_userid(conn, username):
    c = conn.cursor()
    return c.execute("""SELECT userid FROM Users WHERE username = ?;""", (str(username),))


def update_user_mail(conn, userid, mail):
    c = conn.cursor()
    c.execute("""UPDATE Users SET mail = ? WHERE userid = ?;""", (str(mail), str(userid)))


def get_user_history_v2(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT *
    FROM Matches
    WHERE Matches.host = ? OR Matches.friend = ? OR Matches.enemy1 = ? OR Matches.enemy2 = ?;""", (str(userid), str(userid), str(userid), str(userid)))


def get_user_history(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT m1.username, m2.username, m3.username, m4.username, winner, datetime
    FROM Matches
    LEFT OUTER JOIN Users as m1 on m1.userid = Matches.host
    LEFT OUTER JOIN Users as m2 on m2.userid = Matches.friend
    LEFT OUTER JOIN Users as m3 on m3.userid = Matches.enemy1
    LEFT OUTER JOIN Users as m4 on m4.userid = Matches.enemy2
    WHERE host = ? OR friend = ? OR enemy1 = ? OR enemy2 = ?
    ORDER BY datetime DESC;""", (str(userid), str(userid), str(userid), str(userid)))


def get_friends(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT m1.username, friendid FROM Friends
    LEFT OUTER JOIN Users as m1 on m1.userid = Friends.friendid
    WHERE Friends.userid = ?;""", (str(userid),))


def add_friend(conn, userid, friendid):
    c = conn.cursor()
    c.execute("""INSERT INTO Friends (userid, friendid) VALUES (?, ?);""", (str(userid), str(friendid)))


def remove_friend(conn, userid, friendid):
    c = conn.cursor()
    c.execute("""DELETE FROM Friends WHERE userid = ? AND friendid = ?;""", (str(userid), str(friendid)))


def is_friend(conn, userid, friendid):
    c = conn.cursor()
    return c.execute("""SELECT 1 FROM Friends WHERE userid = ? AND friendid = ?;""", (str(userid), str(friendid)))


def update_elo_history(conn, matchid, host_elo_old, friend_elo_old, enemy1_elo_old, enemy2_elo_old, host_elo_new,
                       friend_elo_new, enemy1_elo_new, enemy2_elo_new):
    c = conn.cursor()
    c.execute("""UPDATE Matches SET host_elo_delta = ?, friend_elo_delta = ?, enemy1_elo_delta = ?, enemy2_elo_delta = ? WHERE matchid = ?;""", (
        int(host_elo_new - host_elo_old), int(friend_elo_new - friend_elo_old),
        int(enemy1_elo_new - enemy1_elo_old), int(enemy2_elo_new - enemy2_elo_old), matchid))


def ban_ip(conn, banid, ban_date, reason, ip):
    c = conn.cursor()
    c.execute("""INSERT INTO Bans_IP (banid, ban_date, reason, ip) 
        VALUES (?,?,?,?);""", (str(banid), str(ban_date), str(reason), str(ip)))


def ip_is_banned(conn, ip):
    c = conn.cursor()
    return c.execute("""SELECT 1 FROM Bans_IP WHERE ip = ?;""", (str(ip),))


def user_is_banned(conn, username):
    c = conn.cursor()
    return c.execute("""SELECT 1 FROM Bans_User WHERE userid = ?;""", (str(username),))


def ban_user(conn, banid, userid, ban_date, ban_expire, reason, ip):
    c = conn.cursor()
    log.info('banid: ' + str(banid))
    log.info('userid: ' + str(userid))
    log.info('ban_date: ' + str(ban_date))
    log.info('ban_expire: ' + str(ban_expire))
    log.info('reason: ' + str(reason))
    log.info('ip: ' + str(ip))
    c.execute("""INSERT INTO Bans_User (banid, userid, ban_date, ban_expire, reason, ip) 
            VALUES (?,?,?,?,?,?);""", (str(banid), str(userid), str(ban_date), str(ban_expire), str(reason), str(ip)))
