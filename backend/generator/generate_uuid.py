import uuid as uuid4

from ..validate.is_unique import main as is_unique


def main(conn):
    while True:
        uuid = uuid4.uuid4()
        if is_unique(conn, 'userid', uuid) and is_unique(conn, 'matchid', uuid):
            break
    return str(uuid)
