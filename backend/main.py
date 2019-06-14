import json

from flask import Flask
from flask import request
from flask_cors import CORS
from . import generator, connection, handlers, match, sql, response, log, validate, catch
from .enums import Match, Login, Leaderboard, History, Id, Version, Friends


app = Flask(__name__)
CORS(app)
path = '/home/devking/server/devking.db'


@app.route('/user/create', methods=['POST'])
def router_create_user():
    username = request.form.get('username')
    mail = request.form.get('mail')
    passwd = request.form.get('passwd')
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
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
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        r = handlers.update_mail(conn, username, passwd, mail)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/user/profile', methods=['GET'])
def router_login():
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    device_version = request.args.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        if catch.empty_login(username, passwd):
            connection.kill(conn)
            return response.build(Login.FAILED)
        if handlers.login(conn, username, passwd):
            p = sql.get_profile(conn, username, passwd).fetchall()
            connection.kill(conn)
            return response.build(Login.SUCCESSFUL, p)
        else:
            connection.kill(conn)
            return response.build(Login.FAILED)
    else:
        return response.build(Version.OUTDATED)


@app.route('/match/1v1', methods=['POST'])
def router_start_1v1():
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    winner = request.form.get('winner')
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
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
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        r = match.start_2v2(conn, host, friend, enemy1, enemy2, winner)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/match/pending', methods=['GET'])
def router_pending_matches():
    userid = request.args.get('userid')
    device_version = request.args.get('version')

    if validate.is_correct_version(device_version):
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
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        if handlers.login(conn, username, passwd):
            r = handlers.confirm_match(conn)
        connection.kill(conn)
        return response.build(r)
    else:
        return response.build(Version.OUTDATED)


@app.route('/leaderboard', methods=['GET'])
def router_leaderboard():
    userid = request.args.get('userid')
    device_version = request.args.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        arr = handlers.leaderboard(conn, userid)
        return response.build(Leaderboard.RETRIEVED, arr)
    else:
        return response.build(Version.OUTDATED)


@app.route('/user/history', methods=['GET'])
def router_get_user_history():
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    device_version = request.args.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        if handlers.login(conn, username, passwd):
            h = handlers.user_history(conn, username)
            connection.kill(conn)
            return response.build(History.RETRIEVED, h)
    else:
        return response.build(Version.OUTDATED)


@app.route('/userid', methods=['GET'])
def router_userid_exists():
    userid = request.args.get('userid')
    device_version = request.args.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        if not validate.is_unique(conn, 'userid', userid):
            connection.kill(conn)
            return response.build(Id.EXISTS)
        else:
            connection.kill(conn)
            return response.build(Id.DOESNT_EXIST)
    else:
        return response.build(Version.OUTDATED)


@app.route('/friends', methods=['GET'])
def router_get_friends():
    userid = request.args.get('userid')
    device_version = request.args.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        fl = sql.get_friends(conn, userid).fetchall()
        connection.kill(conn)
        return response.build(Friends.FINE, fl)
    else:
        return response.build(Version.OUTDATED)


@app.route('/friends/add', methods=['POST'])
def router_add_friend():
    userid = request.form.get('userid')
    friendid = request.form.get('friendid')
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        sql.add_friend(conn, userid, friendid)
        connection.kill(conn)
        return response.build(Friends.ADDED)
    else:
        return response.build(Version.OUTDATED)


@app.route('/friends/remove', methods=['DELETE'])
def router_remove_friend():
    userid = request.form.get('userid')
    friendid = request.form.get('friendid')
    device_version = request.form.get('version')

    if validate.is_correct_version(device_version):
        conn = connection.create(path)
        sql.remove_friend(conn, userid, friendid)
        connection.kill(conn)
        return response.build(Friends.REMOVED)
    else:
        return response.build(Version.OUTDATED)
