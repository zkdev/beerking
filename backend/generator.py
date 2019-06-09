import uuid as uuid4

from . import validate


def create_uuid(conn):
    while True:
        uuid = uuid4.uuid4()
        if validate.is_unique(conn, 'userid', uuid) and validate.is_unique(conn, 'matchid', uuid):
            break
    return str(uuid)
