def main(conn, matchid):
    c = conn.cursor()
    c.execute("""DELETE FROM PendingMatches WHERE matchid = ?;""", (str(matchid),))
