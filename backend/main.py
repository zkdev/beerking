from flask import Flask
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS


import generator
import connection
import handlers
import match
import sql
import response
import validate
import log
import security
from enums import Match, Auth, Leaderboard, History, User, Error, Friends, UniqueMode


app = Flask(__name__)
CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20 per minute", "1 per second"],
)
path = '/database/beerking.db'



@app.route('/users/login', methods=['GET'])
def router_login_user():
    log.error("Outdated app version tried to login.", ip=request.remote_addr)
    return response.build(Error.VERSION_OUTDATED)


@app.route('/user/create', methods=['POST'])
@limiter.limit("10 per hour")
def router_create_user():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to create a user.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    username = request.form.get('username')
    mail = request.form.get('mail')
    passwd = request.form.get('passwd')
    arr = [ip, username, mail, passwd]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        userid = generator.create_uuid(conn)
                        r = handlers.create_user(conn, userid, username, mail, passwd)
                        connection.kill(conn)
                        log.info("User created ({})".format(username), ip=request.remote_addr)
                        return response.build(r)

                    else:
                        log.error("Outdated app version tried to create a user.", ip=request.remote_addr)
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/user/mail/update', methods=['PUT'])
@limiter.limit("3 per hour")
def router_update_mail():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to update mail.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    mail = request.form.get('mail')
    arr = [ip, username, mail, passwd]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        r = handlers.update_mail(conn, username, passwd, mail)
                        connection.kill(conn)
                        log.info("User changed email adresse ({0} to {1})".format(username, mail), ip=request.remote_addr)
                        return response.build(r)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/user/profile', methods=['GET'])
@limiter.limit("20 per hour")
def router_auth():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to get profile.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    arr = [ip, username, passwd]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        if validate.catch_empty_auth(username, passwd):
                            connection.kill(conn)
                            log.security("Auth failed, it was empty ({}).".format(username), ip=request.remote_addr)
                            return response.build(Auth.FAILED)
                        if handlers.auth(conn, username, passwd):
                            p = sql.get_profile(conn, username, passwd).fetchall()
                            log.info("User retrieved profile ({}).".format(username), ip=request.remote_addr)
                            connection.kill(conn)
                            return response.build(Auth.SUCCESSFUL, rs=p)
                        else:
                            connection.kill(conn)
                            log.security("Auth failed ({}).".format(username), ip=request.remote_addr)
                            return response.build(Auth.FAILED, server_message='Nickname oder Passwort ist falsch.')

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/match/1v1', methods=['POST'])
@limiter.limit("10 per hour")
def router_start_1v1():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to start 1v1.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    winner = request.form.get('winner')
    arr = [ip, host, enemy, winner]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if security.is_no_sql_injection(arr, request.remote_addr):
            if security.is_no_rdp_attempt(request, request.remote_addr):
                if correct_version:

                    conn = connection.create(path)
                    r = match.start_1v1(conn, host, enemy, winner)
                    connection.kill(conn)
                    log.info("{0} started match vs {1}.".format(host, enemy), ip=request.remote_addr)
                    return response.build(r)

                else:
                    return response.build(Error.VERSION_OUTDATED)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(Error.SECURITY_INCIDENT)
    else:
        return response.build(User.BANNED)


@app.route('/match/2v2', methods=['POST'])
@limiter.limit("10 per hour")
def router_start_2v2():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to start 2v2.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    host = request.form.get('host')
    friend = request.form.get('friend')
    enemy1 = request.form.get('enemy1')
    enemy2 = request.form.get('enemy2')
    winner = request.form.get('winner')
    arr = [ip, host, friend, enemy1, enemy2, winner]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if security.is_no_sql_injection(arr, request.remote_addr):
            if security.is_no_rdp_attempt(request, request.remote_addr):
                if correct_version:

                    conn = connection.create(path)
                    r = match.start_2v2(conn, host, friend, enemy1, enemy2, winner)
                    connection.kill(conn)
                    log.info("{0} and {1} started 2v2 vs {2} and {3}.".format(host, friend, enemy1, enemy2), ip=request.remote_addr)
                    return response.build(r)

                else:
                    return response.build(Error.VERSION_OUTDATED)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(Error.SECURITY_INCIDENT)
    else:
        return response.build(User.BANNED)


@app.route('/match/pending', methods=['GET'])
@limiter.limit("25 per hour")
def router_get_pending_matches():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to retrieve pending matches.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    userid = request.args.get('userid')
    arr = [ip, userid]
    conn = connection.create(path)
    username = sql.get_username(conn, userid).fetchone()[0]

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        ja = match.get_pending_matches(conn, userid)
                        connection.kill(conn)
                        log.info("{} retrieved pending matches.".format(username), ip=request.remote_addr)
                        return response.build(Match.RECEIVED, ja)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/match/confirm', methods=['POST'])
@limiter.limit("10 per hour")
def router_confirm_match():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to confirm match.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    arr = [ip, username, passwd]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        if handlers.auth(conn, username, passwd):
                            r = handlers.confirm_match(conn)
                            log.info("{} confirmed match.".format(username), ip=request.remote_addr)
                        else:
                            log.security("Auth failed at match confirmation ({}).".format(username), ip=request.remote_addr)
                            connection.kill(conn)
                            return response.build(Auth.FAILED)
                        connection.kill(conn)
                        return response.build(r)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/leaderboard', methods=['GET'])
@limiter.limit("35 per hour")
def router_get_leaderboard():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to get leaderboard.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    userid = request.args.get('userid')
    arr = [ip, userid]
    conn = connection.create(path)
    username = sql.get_username(conn, userid).fetchone()[0]

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        arr = handlers.leaderboard(conn, userid)
                        log.info("{} retrieved leaderboard.".format(username), ip=request.remote_addr)
                        return response.build(Leaderboard.RETRIEVED, arr)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/user/history', methods=['GET'])
@limiter.limit("35 per hour")
def router_get_user_history():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to retrieve history.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    arr = [ip, username, passwd]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        if handlers.auth(conn, username, passwd):
                            h = handlers.user_history(conn, username)
                            connection.kill(conn)
                            log.info("{} retrieved history.".format(username), ip=request.remote_addr)
                            return response.build(History.RETRIEVED, h)
                        else:
                            log.security("Auth failed at history retrieving ({}).".format(username),
                                         ip=request.remote_addr)
                            connection.kill(conn)
                            return response.build(Auth.FAILED)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/check/userid', methods=['GET'])
@limiter.limit("20 per hour")
def router_check_if_userid_exists():
    userid = request.args.get('userid')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to check userid.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    arr = [ip, userid]
    conn = connection.create(path)

    if not security.ip_is_banned(conn, ip):
        if security.is_no_sql_injection(arr, request.remote_addr):
            if security.is_no_rdp_attempt(request, request.remote_addr):
                if correct_version:

                    conn = connection.create(path)
                    if not validate.is_unique(conn, UniqueMode.USER_ID, userid):
                        connection.kill(conn)
                        log.info("{} exists.".format(userid), ip=request.remote_addr)
                        return response.build(User.ID_EXISTS)
                    else:
                        log.info("{} doesn't exist.".format(userid), ip=request.remote_addr)
                        return response.build(User.ID_DOESNT_EXIST)

                else:
                    return response.build(Error.VERSION_OUTDATED)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(Error.SECURITY_INCIDENT)
    else:
        return response.build(User.BANNED)


@app.route('/friends', methods=['GET'])
@limiter.limit("35 per hour")
def router_get_friends():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to retrieve friends.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    userid = request.args.get('userid')
    arr = [ip, userid]
    conn = connection.create(path)
    username = sql.get_username(conn, userid).fetchone()[0]

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        fl = sql.get_friends(conn, userid).fetchall()
                        connection.kill(conn)
                        log.info("{} retrieved friends.".format(username), ip=request.remote_addr)
                        return response.build(Friends.RETRIEVED, fl)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/friends/add', methods=['POST'])
@limiter.limit("20 per hour")
def router_add_friend():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to add friends.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    userid = request.form.get('userid')
    friendname = request.form.get('friendname')
    arr = [ip, userid, friendname]
    conn = connection.create(path)
    username = sql.get_username(conn, userid).fetchone()[0]

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        r = handlers.add_friend(conn, userid, friendname)
                        connection.kill(conn)
                        log.info("{0} added {1} as friend.".format(username, friendname), ip=request.remote_addr)
                        return response.build(r)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)


@app.route('/friends/remove', methods=['DELETE'])
@limiter.limit("20 per hour")
def router_remove_friend():
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        log.error("Outdated app version tried to remove friend.", ip=request.remote_addr)
        return response.build(Error.VERSION_OUTDATED)

    ip = request.remote_addr
    userid = request.form.get('userid')
    friendname = request.form.get('friendname')
    arr = [ip, userid, friendname]
    conn = connection.create(path)
    username = sql.get_username(conn, userid).fetchone()[0]

    if not security.ip_is_banned(conn, ip):
        if not security.user_is_banned(conn, username, request.remote_addr):
            if security.is_no_sql_injection(arr, request.remote_addr):
                if security.is_no_rdp_attempt(request, request.remote_addr):
                    if correct_version:

                        conn = connection.create(path)
                        handlers.remove_friend(conn, userid, friendname)
                        connection.kill(conn)
                        log.info("{0} removed {1} as friend.".format(username, friendname), ip=request.remote_addr)
                        return response.build(Friends.REMOVED)

                    else:
                        return response.build(Error.VERSION_OUTDATED)
                else:
                    return response.build(Error.SECURITY_INCIDENT)
            else:
                return response.build(Error.SECURITY_INCIDENT)
        else:
            return response.build(User.BANNED)
    else:
        return response.build(User.BANNED)
