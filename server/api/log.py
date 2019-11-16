import connection
import config
import datetime
import sql


def info(msg, ip=""):
    conn = connection.create(config.database)
    loglevel = "INFO"
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('[\033[1;32;40m{0}\033[0;37;40m][{1}]: {2}'.format(loglevel, date, str(msg)), flush=True)
    sql.insert_log(conn, loglevel, date, msg, ip)
    connection.kill(conn)


def error(msg, ip=""):
    conn = connection.create(config.database)
    loglevel = "ERROR"
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('[\033[0;31;40m{0}\033[0;37;40m][{1}]: {2}'.format(loglevel, date, str(msg)), flush=True)
    sql.insert_log(conn, loglevel, date, msg, ip)
    connection.kill(conn)


def security(msg, ip=""):
    conn = connection.create(config.database)
    loglevel = "SECURITY"
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('[\033[1;31;40m{0}\033[0;37;40m][{1}]: {2}'.format(loglevel, date, str(msg)), flush=True)
    sql.insert_log(conn, loglevel, date, msg, ip)
    connection.kill(conn)
