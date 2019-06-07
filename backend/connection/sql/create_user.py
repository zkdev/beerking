def main(c, userid, username, mail, passwd, elo):
    return c.execute("""INSERT INTO users(userid, username, mail, passwd, elo) 
        VALUES (?,?,?,?,?);""", (str(userid), str(username), str(mail), str(passwd), int(elo)))