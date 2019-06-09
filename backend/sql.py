import datetime


def get_match(conn, matchid):
    c = conn.cursor()
    return c.execute("""SELECT * FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))


def is_unique(c, key, value):

    # somehow I'm not able to provide the key as a binding as well
    # so I use this ugly if statement to prepare the sql statement

    sql = """SELECT 1 FROM users WHERE userid = ?;"""
    if key is 'username':
        sql = """SELECT 1 FROM users WHERE username = ?;"""
    return c.execute(sql, (str(value),))


def leaderboard(conn):
    c = conn.cursor()
    return c.execute("""SELECT username, elo FROM Users ORDER BY elo ASC;""")


def login(c, username, passwd):
    return c.execute("""SELECT 1 FROM users WHERE username = ? and passwd = ?;"""
                  , (str(username), str(passwd))).fetchone()


def remove_pending_match(conn, matchid):
    c = conn.cursor()
    c.execute("""DELETE FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))


def start_1v1(conn, matchid, host, enemy, winner):
    c = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return c.execute("""INSERT INTO PendingMatches(matchid, host, enemy1, winner, datetime) 
        VALUES (?,?,?,?,?);""", (str(matchid), str(host), str(enemy), str(winner), str(date)))


def start_2v2(conn, matchid, host, friend, enemy1, enemy2, winner):
    c = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return c.execute("""INSERT INTO PendingMatches(matchid, host, friend, enemy1, enemy2, winner, datetime) 
        VALUES (?,?,?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2),
                                     str(winner), str(date)))


def get_profile(c, username, passwd):
    return c.execute("""SELECT userid, mail FROM Users WHERE username = ? AND passwd = ?;""", (str(username), str(passwd)))


def get_username(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT username FROM Users WHERE userid = ?;""", (str(userid),))


def get_pending_matches(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT matchid, host, winner, datetime, username FROM PendingMatches, Users WHERE Users.userid = host AND (enemy1 = ? OR enemy2 = ?);""", (str(userid), str(userid)))


def create_user(c, userid, username, mail, passwd, elo):
    return c.execute("""INSERT INTO users(userid, username, mail, passwd, elo) 
        VALUES (?,?,?,?,?);""", (str(userid), str(username), str(mail), str(passwd), int(elo)))


def confirm_match(conn, matchid, host, friend, enemy1, enemy2, winner, datetime):
    c = conn.cursor()
    c.execute("""INSERT INTO Matches(matchid, host, friend, enemy1, enemy2, winner, datetime) 
        VALUES (?,?,?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2), int(winner), str(datetime)))
