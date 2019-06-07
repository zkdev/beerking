def main(conn, matchid):
    c = conn.cursor()
    return c.execute("""SELECT * FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))
