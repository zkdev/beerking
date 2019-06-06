def main(c, username, passwd):
    return c.execute("""SELECT userid, mail FROM Users WHERE username = ? AND passwd = ?;""", (str(username), str(passwd)))
