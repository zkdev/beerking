def main(c, uuid, username, mail, passwd):
    return c.execute("""INSERT INTO users(uuid, username, mail, passwd) 
        VALUES (?,?,?,?);""", (str(uuid), str(username), str(mail), str(passwd)))