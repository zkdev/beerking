import uuid as uuid4

from ..validate.is_unique import main as is_unique


def main(conn):
    while True:
        uuid = uuid4.uuid4()
        if is_unique(conn, 'uuid', uuid):
            break
    return str(uuid)
