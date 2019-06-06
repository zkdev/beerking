from ...generator.generate_uuid import main as gen_uuid


def main(conn, host, friend, enemy1, enemy2):
    c = conn.cursor()
    matchid = gen_uuid(conn)
    return c.execute("""INSERT INTO PendingMatches(matchid, host, friend, enemy1, enemy2) 
        VALUES (?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2)))
