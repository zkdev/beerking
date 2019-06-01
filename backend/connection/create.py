import sqlite3


def main(path_to_db):
    return sqlite3.connect(path_to_db)
