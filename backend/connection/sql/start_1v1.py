import datetime

from ...generator.generate_uuid import main as gen_uuid


def main(conn, host, enemy, winner):
    c = conn.cursor()
    matchid = gen_uuid(conn)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return c.execute("""INSERT INTO PendingMatches(matchid, host, enemy1, winner, datetime) 
        VALUES (?,?,?,?,?);""", (str(matchid), str(host), str(enemy), str(winner), str(date)))
