import json

from flask import Flask
from flask import request
from flask_cors import CORS
from . import generator, connection, handlers, match, sql, response, log, validate
from .enums import Match, Login, Leaderboard, History, Id, Error


app = Flask(__name__)
CORS(app)
path = '/home/beerking/server/beerking.db'


@app.route('/users/creation', methods=['POST'])
def router_create_user():
    conn = connection.create(path)
    userid = generator.create_uuid(conn)
    username = request.form.get('username')
    mail = request.form.get('mail')
    passwd = str(request.form.get('passwd'))
    r = handlers.create_user(conn, userid, username, mail, passwd)
    connection.kill(conn)
    return response.build(r)


@app.route('/users/mail/update', methods=['PUT'])
def router_update_mail():
    conn = connection.create(path)
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    mail = request.form.get('mail')
    r = handlers.login(conn, username, passwd)
    userid = handlers.get_profile(r, conn, username, passwd).fetchone()[0]
    if r is Login.SUCCESSFUL:
        r = sql.update_user_mail(conn, userid, mail)
    else:
        r = Login.PASSWD_WRONG
    connection.kill(conn)
    return response.build(r)


@app.route('/users/login', methods=['GET'])
def router_login():
    conn = connection.create(path)
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    r = handlers.login(conn, username, passwd)
    p = handlers.get_profile(r, conn, username, passwd).fetchall()
    connection.kill(conn)
    return response.build(r, p)


@app.route('/match/1v1', methods=['POST'])
def router_start_1v1():
    conn = connection.create(path)
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    winner = request.form.get('winner')
    r = match.start_1v1(conn, host, enemy, winner)
    connection.kill(conn)
    return response.build(r)


@app.route('/match/2v2', methods=['POST'])
def router_start_2v2():
    conn = connection.create(path)
    host = request.form.get('host')
    friend = request.form.get('friend')
    enemy1 = request.form.get('enemy1')
    enemy2 = request.form.get('enemy2')
    winner = request.form.get('winner')
    r = match.start_2v2(conn, host, friend, enemy1, enemy2, winner)
    connection.kill(conn)
    return response.build(r)


@app.route('/match/pending', methods=['GET'])
def router_pending_matches():
    conn = connection.create(path)
    userid = request.args.get('userid')
    ja = match.get_pending_matches(conn, userid)
    connection.kill(conn)
    return response.build(Match.RECEIVED, ja)


@app.route('/match/confirm', methods=['POST'])
def router_confirm_match():
    conn = connection.create(path)
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    r = Error.ERROR
    if handlers.login(conn, username, passwd) is Login.SUCCESSFUL:
        for single_match in json.loads(request.form.get('matches')):
            if single_match.get('confirmed') is True:
                matchid = single_match.get('matchid')
                r = match.confirm_match(conn, matchid)
            sql.remove_pending_match(conn, matchid)
        connection.kill(conn)
        return response.build(r)
    else:
        log.error('An unexpected error occurred (login error at match confirmation)')


@app.route('/leaderboard', methods=['GET'])
def router_leaderboard():
    conn = connection.create(path)
    leaderboard = sql.leaderboard(conn).fetchall()
    arr = []
    for entry in leaderboard:
        username = entry[0]
        elo = entry[1]
        arr.append({"username": username, "elo": elo})
    connection.kill(conn)
    return response.build(Leaderboard.FINE, arr)


@app.route('/users/history', methods=['GET'])
def router_get_user_history():
    conn = connection.create(path)
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    r = handlers.login(conn, username, passwd)
    if r is Login.SUCCESSFUL:
        userid = sql.get_userid(conn, username).fetchone()[0]
        h = sql.get_user_history(conn, userid).fetchall()
        connection.kill(conn)
        return response.build(History.FINE, h)
    else:
        log.error('login failed at retrieving user history')


@app.route('/userid', methods=['GET'])
def router_userid_exists():
    conn = connection.create(path)
    userid = request.args.get('userid')
    if not validate.is_unique(conn, 'userid', userid):
        connection.kill(conn)
        return response.build(Id.EXISTS)
    else:
        connection.kill(conn)
        return response.build(Id.DOESNT_EXIST)
