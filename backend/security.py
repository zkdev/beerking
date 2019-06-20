import datetime


from . import connection, log, sql, generator


path = '/home/devking/server/database/devking.db'


def is_no_sql_injection(arr):
    identifier = ['DROP', 'TABLE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', ';', '%', '--', '\'']
    for value in arr:
        for element in identifier:
            if element in value:
                log.security('Possible SQL injection detected. Trigger: ' + str(element))
                log.security('IP ban executed. IP: ' + str(arr[0]))
                ban_ip(arr[0], 'Possible SQL injection detected, keyword: ' + str(element))
                return False
    return True


def ban_user(userid, period, reason, ip):
    conn = connection.create(path)
    banid = generator.create_uuid(conn)
    ban_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ban_expire = datetime.datetime.now() + datetime.timedelta(days=int(period))
    ban_expire = ban_expire.strftime("%Y-%m-%d %H:%M:%S")
    sql.ban_user(conn, banid, userid, ban_date, ban_expire, reason, ip)
    connection.kill(conn)


def ban_ip(ip, reason):
    conn = connection.create(path)
    banid = generator.create_uuid(conn)
    ban_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql.ban_ip(conn, banid, ban_date, reason, ip)
    connection.kill(conn)


def ip_is_banned(conn, ip):
    if sql.ip_is_banned(conn, ip).fetchone() is None:
        return False
    else:
        log.security('Banned ip tried to log in.')
        log.security('IP: ' + str(ip))
        return True


def user_is_banned(conn, username):
    userid = sql.get_userid(conn, username)
    if sql.user_is_banned(conn, userid).fetchone() is None:
        return False
    else:
        log.security('Banned user tried to log in.')
        log.security('Username: ' + str(username))
        return True
