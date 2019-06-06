def main(c, userid, username, mail, passwd):
    return c.execute("""INSERT INTO users(userid, username, mail, passwd) 
        VALUES (?,?,?,?);""", (str(userid), str(username), str(mail), str(passwd)))