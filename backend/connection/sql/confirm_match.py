def main(conn, matchid, host, friend, enemy1, enemy2, winner, datetime):
    c = conn.cursor()
    c.execute("""INSERT INTO Matches(matchid, host, friend, enemy1, enemy2, winner, datetime) 
        VALUES (?,?,?,?,?,?,?);""", (str(matchid), str(host), str(friend), str(enemy1), str(enemy2), int(winner), str(datetime)))
