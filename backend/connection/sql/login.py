def main(c, username, passwd):
    return c.execute("""SELECT 1 FROM users WHERE username = ? and passwd = ?;"""
                  , (str(username), str(passwd))).fetchone()