from ..connection.sql.is_unique import main as is_unique


def main(conn, key, value):
    c = conn.cursor()
    r = is_unique(c, key, value)
    if r is None:
        return True
    else:
        return False
