from ...generator.generate_uuid import main as gen_uuid


def main(conn, host, enemy):
    c = conn.cursor()
    matchid = gen_uuid(conn)
    return c.execute("""INSERT INTO PendingMatches(matchid, host, enemy1, enemy1_accepted) 
        VALUES (?,?,?,?);""", (str(matchid), str(host), str(enemy), int(1)))
