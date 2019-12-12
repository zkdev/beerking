from flask import Flask
from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from middleware import Middleware


import generator
import config
import connection
import handlers
import match
import sql
import response as response
import validate
import log
from enums import UniqueMode


app = Flask(__name__)
CORS(app)
app.wsgi_app = Middleware(app.wsgi_app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20 per minute", "1 per second"],
)


@app.route('/status', methods=["GET"])
@limiter.limit("60 per minute")
def router_status():
    log.info("backend status checked", ip=request.remote_addr)
    return response.build({"status": "available"}, statuscode=200)


@app.route('/users/login', methods=['GET'])
def router_login_user():
    log.error("Outdated app version tried to login.", ip=request.remote_addr)
    return response.build({"outdated_app_version": True,
                        "status": config.text["outdated"]}, statuscode=403)


@app.route('/user/create', methods=['POST'])
@limiter.limit("10 per hour")
def router_create_user():
    username = request.form.get('username')
    mail = request.form.get('mail')
    passwd = request.form.get('passwd')
    conn = connection.create(config.database)

    userid = generator.create_uuid(conn)
    resp = handlers.create_user(conn, userid, username, mail, passwd)
    connection.kill(conn)
    log.info("User created ({})".format(username), ip=request.remote_addr)
    return resp


@app.route('/user/mail/update', methods=['PUT'])
@limiter.limit("3 per hour")
def router_update_mail():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    mail = request.form.get('mail')
    conn = connection.create(config.database)
    resp = handlers.update_mail(conn, username, passwd, mail)
    connection.kill(conn)
    log.info("User changed email adresse ({0} to {1})".format(username, mail), ip=request.remote_addr)
    return resp


@app.route('/user/profile', methods=['GET'])
@limiter.limit("20 per hour")
def router_auth():
    username = request.args.get('username')
    passwd = request.args.get('passwd')
    conn = connection.create(config.database)

    if validate.catch_empty_auth(username, passwd):
        connection.kill(conn)
        log.security("Auth failed, it was empty ({}).".format(username), ip=request.remote_addr)
        return response.build({"auth": False}, statuscode=401)
    if handlers.auth(conn, username, passwd):
        profile = sql.get_profile(conn, username, passwd).fetchall()
        log.info("User retrieved profile ({}).".format(username), ip=request.remote_addr)
        connection.kill(conn)
        return response.build({"auth": True, "userid": profile[0][0], "mail": profile[0][1]}, statuscode=200)
    else:
        connection.kill(conn)
        log.security("Auth failed ({}).".format(username), ip=request.remote_addr)
        return response.build({"auth": False, "status": config.text["wrong_credentials"]}, statuscode=401)


@app.route('/match/1v1', methods=['POST'])
@limiter.limit("10 per hour")
def router_start_1v1():
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    winner = request.form.get('winner')

    conn = connection.create(config.database)
    resp = match.start_1v1(conn, host, enemy, winner)
    connection.kill(conn)
    log.info("{0} started match vs {1}.".format(host, enemy), ip=request.remote_addr)
    return resp


@app.route('/match/2v2', methods=['POST'])
@limiter.limit("10 per hour")
def router_start_2v2():
    host = request.form.get('host')
    friend = request.form.get('friend')
    enemy1 = request.form.get('enemy1')
    enemy2 = request.form.get('enemy2')
    winner = request.form.get('winner')

    conn = connection.create(config.database)
    resp = match.start_2v2(conn, host, friend, enemy1, enemy2, winner)
    connection.kill(conn)
    log.info("{0} and {1} started 2v2 vs {2} and {3}.".format(host, friend, enemy1, enemy2), ip=request.remote_addr)
    return resp


@app.route('/match/pending', methods=['GET'])
@limiter.limit("25 per hour")
def router_get_pending_matches():
    userid = request.args.get('userid')
    conn = connection.create(config.database)
    username = sql.get_username(conn, userid).fetchone()[0]

    conn = connection.create(config.database)
    resp = match.get_pending_matches(conn, userid)
    connection.kill(conn)
    log.info("{} retrieved pending matches.".format(username), ip=request.remote_addr)
    return resp


@app.route('/match/confirm', methods=['POST'])
@limiter.limit("10 per hour")
def router_confirm_match():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    conn = connection.create(config.database)
    if handlers.auth(conn, username, passwd):
        resp = handlers.confirm_match(conn)
        log.info("{} confirmed match.".format(username), ip=request.remote_addr)
    else:
        log.security("Auth failed at match confirmation ({}).".format(username), ip=request.remote_addr)
        connection.kill(conn)
        return response.build({"auth": False}, statuscode=401)
    connection.kill(conn)
    return resp


@app.route('/leaderboard', methods=['GET'])
@limiter.limit("35 per hour")
def router_get_leaderboard():
    userid = request.args.get('userid')
    conn = connection.create(config.database)
    username = sql.get_username(conn, userid).fetchone()[0]

    conn = connection.create(config.database)
    arr = handlers.leaderboard(conn, userid)
    log.info("{} retrieved leaderboard.".format(username), ip=request.remote_addr)
    return response.build({"leaderboard": arr}, statuscode=200)


@app.route('/user/history', methods=['GET'])
@limiter.limit("35 per hour")
def router_get_user_history():
    username = request.args.get('username')
    passwd = request.args.get('passwd')

    conn = connection.create(config.database)
    if handlers.auth(conn, username, passwd):
        resp = handlers.user_history(conn, username)
        connection.kill(conn)
        log.info("{} retrieved history.".format(username), ip=request.remote_addr)
        return resp
    else:
        log.security("Auth failed at history retrieving ({}).".format(username),
                     ip=request.remote_addr)
        connection.kill(conn)
        return response.build({"auth": False}, statuscode=401)


@app.route('/check/userid', methods=['GET'])
@limiter.limit("20 per hour")
def router_check_if_userid_exists():
    userid = request.args.get('userid')
    conn = connection.create(config.database)
    if not validate.is_unique(conn, UniqueMode.USER_ID, userid):
        connection.kill(conn)
        log.info("{} exists.".format(userid), ip=request.remote_addr)
        return response.build({"userid_exists": True}, statuscode=200)
    else:
        log.info("{} doesn't exist.".format(userid), ip=request.remote_addr)
        return response.build({"userid_exists": False}, statuscode=401)


@app.route('/friends', methods=['GET'])
@limiter.limit("35 per hour")
def router_get_friends():
    userid = request.args.get('userid')
    conn = connection.create(config.database)
    username = sql.get_username(conn, userid).fetchone()[0]

    conn = connection.create(config.database)
    resp = handlers.get_friends(conn, userid)
    connection.kill(conn)
    log.info("{} retrieved friends.".format(username), ip=request.remote_addr)
    return resp


@app.route('/friends/add', methods=['POST'])
@limiter.limit("20 per hour")
def router_add_friend():
    userid = request.form.get('userid')
    friendname = request.form.get('friendname')
    conn = connection.create(config.database)
    username = sql.get_username(conn, userid).fetchone()[0]

    conn = connection.create(config.database)
    resp = handlers.add_friend(conn, userid, friendname)
    connection.kill(conn)
    log.info("{0} added {1} as friend.".format(username, friendname), ip=request.remote_addr)
    return resp


@app.route('/friends/remove', methods=['DELETE'])
@limiter.limit("20 per hour")
def router_remove_friend():
    userid = request.form.get('userid')
    friendname = request.form.get('friendname')
    conn = connection.create(config.database)
    username = sql.get_username(conn, userid).fetchone()[0]

    conn = connection.create(config.database)
    handlers.remove_friend(conn, userid, friendname)
    connection.kill(conn)
    log.info("{0} removed {1} as friend.".format(username, friendname), ip=request.remote_addr)
    return response.build({"friend_removed": True}, statuscode=200)
