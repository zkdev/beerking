import logger.log as log


def main(conn, key, value):
    c = conn.cursor()
    sql = """SELECT 1 FROM users WHERE uuid = ?;"""

    # somehow I'm not able to provide the key as a binding as well
    # so I use this ugly if statement to prepare the sql statement
    if key is 'username':
        sql = """SELECT 1 FROM users WHERE username = ?;"""

    c.execute(sql, (str(value),))
    r = c.fetchone()
    log.info('========================')
    log.info('key: ' + str(key))
    log.info('value: ' + str(value))
    if r is None:
        log.info('is unique')
        log.info('========================')
        return True
    else:
        log.info('is not unique')
        log.info('========================')
        return False
