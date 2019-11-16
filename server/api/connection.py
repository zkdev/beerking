import sqlite3


def create(path_to_db):
    return sqlite3.connect(path_to_db)


def kill(conn):
    conn.commit()
    conn.close()
