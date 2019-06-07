def main(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT matchid, host, winner, datetime, username FROM PendingMatches, Users WHERE Users.userid = host AND (enemy1 = ? OR enemy2 = ?);""", (str(userid), str(userid)))
