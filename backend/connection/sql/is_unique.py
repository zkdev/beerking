def main(c, key, value):

    # somehow I'm not able to provide the key as a binding as well
    # so I use this ugly if statement to prepare the sql statement

    sql = """SELECT 1 FROM users WHERE userid = ?;"""
    if key is 'username':
        sql = """SELECT 1 FROM users WHERE username = ?;"""
    return c.execute(sql, (str(value),))
