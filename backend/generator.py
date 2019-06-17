import uuid as uuid4

from . import validate
from .enums import UniqueMode


def create_uuid(conn):
    while True:
        uuid = uuid4.uuid4()
        if validate.is_unique(conn, UniqueMode.USER_ID, uuid) and validate.is_unique(conn, UniqueMode.MATCH_ID, uuid):
            break
    return str(uuid)
