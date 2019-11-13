import connection
import datetime
import sql

path = '/database/beerking.db'

def info(msg, ip=""):
    conn = connection.create(path)
    loglevel = "INFO"
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('[\033[1;32;40m' + loglevel + '\033[0;37;40m][' + date + ']: ' + str(msg), flush=True)
    sql.insert_log(conn, loglevel, date, msg, ip)
    connection.kill(conn)


def error(msg, ip=""):
    conn = connection.create(path)
    loglevel = "ERROR"
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('[\033[0;31;40m' + loglevel + '\033[0;37;40m][' + date + ']: ' + str(msg), flush=True)
    sql.insert_log(conn, loglevel, date, msg, ip)
    connection.kill(conn)


def security(msg, ip=""):
    conn = connection.create(path)
    loglevel = "SECURITY"
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('[\033[1;31;40m' + loglevel + '\033[0;37;40m][' + date + ']: ' + str(msg), flush=True)
    sql.insert_log(conn, loglevel, date, msg, ip)
    connection.kill(conn)
