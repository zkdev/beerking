import datetime

from ...generator.generate_uuid import main as gen_uuid


def main(conn, host, friend, enemy1, enemy2, winner):
    c = conn.cursor()
    matchid = gen_uuid(conn)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return c.execute("""INSERT INTO PendingMatches(matchid, host, friend, enemy1, enemy2, winner, datetime) 
        VALUES (?,?,?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2),
                                     str(winner), str(date)))
