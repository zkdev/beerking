import datetime
import connection
import log
import sql
import generator

path = '/home/devking/server/database/devking.db'


def is_no_sql_injection(arr, ip):
    identifier = ['DROP', 'TABLE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', ';', '%', '--', '\'']
    for value in arr:
        for element in identifier:
            if element == value:
                log.security('Possible SQL injection detected. Trigger: ' + str(element), ip=ip)
                log.security('IP ban executed. IP: ' + str(arr[0]), ip=ip)
                ban_ip(arr[0], 'Possible SQL injection detected, keyword: ' + str(element))
                return False
    return True


def is_no_rdp_attempt(request, ip):
    if request.form.get('mstshash') is None:
        return True
    else:
        log.security('Possible RDP attempt detected. Trigger: ' + str(request.form.get('mstshash')), ip=ip)
        log.security('IP ban executed. IP: ' + str(request.remote_addr), ip=ip)
        ban_ip(request.remote_addr, 'Possible RDP attempt detected, keyword: ' + str(request.form.get('mstshash')))
        return False


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
        log.security('Banned ip tried to log in ({}).'.format(ip), ip=ip)
        return True


def user_is_banned(conn, username, ip):
    userid = sql.get_userid(conn, username)
    if sql.user_is_banned(conn, userid).fetchone() is None:
        return False
    else:
        log.security('Banned user tried to log in ({}).'.format(username), ip=ip)
        return True
