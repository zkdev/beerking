def main(conn, userid):
    c = conn.cursor()
    return c.execute("""SELECT username FROM Users WHERE userid = ?;""", (str(userid)))
