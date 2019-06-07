def main(conn):
    c = conn.cursor()
    return c.execute("""SELECT username, elo FROM Users ORDER BY elo ASC;""")