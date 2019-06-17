from deprecated import deprecated
from flask import Flask
from flask import request
from flask_cors import CORS
from . import generator, connection, handlers, match, sql, response, validate, catch
from .enums import Match, Auth, Leaderboard, History, User, Version, Friends, UniqueMode


app = Flask(__name__)
CORS(app)
path = '/home/devking/server/devking.db'


@deprecated
@app.route('/users/login', methods=['GET'])
def router_login_user():
    return response.build(Version.OUTDATED)


@app.route('/user/create', methods=['POST'])
def router_create_user():
    username = request.form.get('username')
    mail = request.form.get('mail')
    passwd = request.form.get('passwd')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        userid = generator.create_uuid(conn)
        r = handlers.create_user(conn, userid, username, mail, passwd)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/user/mail/update', methods=['PUT'])
def router_update_mail():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    mail = request.form.get('mail')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        r = handlers.update_mail(conn, username, passwd, mail)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/user/profile', methods=['GET'])
def router_auth():
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        if validate.catch_empty_auth(username, passwd):
            connection.kill(conn)
            return response.build(Auth.FAILED)
        if handlers.auth(conn, username, passwd):
            p = sql.get_profile(conn, username, passwd).fetchall()
            connection.kill(conn)
            return response.build(Auth.SUCCESSFUL, rs=p)
        else:
            connection.kill(conn)
            return response.build(Auth.FAILED, server_message='Nickname oder Passwort ist falsch.')
    else:
        return response.build(Version.OUTDATED)


@app.route('/match/1v1', methods=['POST'])
def router_start_1v1():
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    winner = request.form.get('winner')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        r = match.start_1v1(conn, host, enemy, winner)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/match/2v2', methods=['POST'])
def router_start_2v2():
    host = request.form.get('host')
    friend = request.form.get('friend')
    enemy1 = request.form.get('enemy1')
    enemy2 = request.form.get('enemy2')
    winner = request.form.get('winner')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        r = match.start_2v2(conn, host, friend, enemy1, enemy2, winner)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/match/pending', methods=['GET'])
def router_get_pending_matches():
    userid = request.args.get('userid')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        ja = match.get_pending_matches(conn, userid)
        connection.kill(conn)
        return response.build(Match.RECEIVED, ja)
    else:
        return response.build(Version.OUTDATED)


@app.route('/match/confirm', methods=['POST'])
def router_confirm_match():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        if handlers.auth(conn, username, passwd):
            r = handlers.confirm_match(conn)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/leaderboard', methods=['GET'])
def router_get_leaderboard():
    userid = request.args.get('userid')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        arr = handlers.leaderboard(conn, userid)
        return response.build(Leaderboard.RETRIEVED, arr)
    else:
        return response.build(Version.OUTDATED)


@app.route('/user/history', methods=['GET'])
def router_get_user_history():
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        if handlers.auth(conn, username, passwd):
            h = handlers.user_history(conn, username)
            connection.kill(conn)
            return response.build(History.RETRIEVED, h)
    else:
        return response.build(Version.OUTDATED)


@app.route('/check/userid', methods=['GET'])
def router_check_if_userid_exists():
    userid = request.args.get('userid')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        if not validate.is_unique(conn, UniqueMode.USER_ID, userid):
            connection.kill(conn)
            return response.build(User.ID_EXISTS)
        else:
            connection.kill(conn)
            return response.build(User.ID_DOESNT_EXIST)
    else:
        return response.build(Version.OUTDATED)


@app.route('/friends', methods=['GET'])
def router_get_friends():
    userid = request.args.get('userid')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        fl = sql.get_friends(conn, userid).fetchall()
        connection.kill(conn)
        return response.build(Friends.RETRIEVED, fl)
    else:
        return response.build(Version.OUTDATED)


@app.route('/friends/add', methods=['POST'])
def router_add_friend():
    userid = request.form.get('userid')
    friendname = request.form.get('friendname')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        r = handlers.add_friend(conn, userid, friendname)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/friends/remove', methods=['DELETE'])
def router_remove_friend():
    userid = request.form.get('userid')
    friendname = request.form.get('friendname')
    device_version = request.headers.get('version')

    try:
        correct_version = validate.is_correct_version(device_version)
    except TypeError:
        return response.build(Version.OUTDATED)

    if correct_version:
        conn = connection.create(path)
        handlers.remove_friend(conn, userid, friendname)
        connection.kill(conn)
        return response.build(Friends.REMOVED)
    else:
        return response.build(Version.OUTDATED)
