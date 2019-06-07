import json

from flask import Flask
from flask import request
from flask_cors import CORS
from .generator.generate_uuid import main as uuid4
from .connection.create import main as create_conn
from .connection.kill import main as kill_conn
from .handlers.create_user.main import main as create_user
from .handlers.respones.main import main as response
from .match import match_1v1, match_2v2, get_pending_matches, confirm_match
from .handlers.profile.main import main as profile
from .enums.enums import Match, Login, Leaderboard
from .handlers.login.main import main as login
from .connection.sql.remove_pending_match import main as remove_pending_match
from elo import rate_1vs1
from .connection.sql.leaderboard import main as leaderboard


app = Flask(__name__)
CORS(app)
path = '/root/BeerKing/BeerKing.db'


@app.route('/users/creation', methods=['POST'])
def router_create_user():
    conn = create_conn(path)
    userid = uuid4(conn)
    username = request.form.get('username')
    mail = request.form.get('mail')
    passwd = str(request.form.get('passwd'))
    r = create_user(conn, userid, username, mail, passwd)
    kill_conn(conn)
    return response(r)


@app.route('/users/login', methods=['GET'])
def router_login():
    conn = create_conn(path)
    username = request.args.get('username')
    passwd = str(request.args.get('passwd')).lower()
    r = login(conn, username, passwd)
    p = profile(r, conn, username, passwd).fetchall()
    kill_conn(conn)
    return response(r, p)


@app.route('/match/1v1', methods=['POST'])
def router_start_1v1():
    conn = create_conn(path)
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    winner = request.form.get('winner')
    r = match_1v1(conn, host, enemy, winner)
    kill_conn(conn)
    return response(r)


@app.route('/match/2v2', methods=['POST'])
def router_start_2v2():
    conn = create_conn(path)
    host = request.form.get('host')
    friend = request.form.get('friend')
    enemy1 = request.form.get('enemy1')
    enemy2 = request.form.get('enemy2')
    winner = request.form.get('winner')
    r = match_2v2(conn, host, friend, enemy1, enemy2, winner)
    kill_conn(conn)
    return response(r)


@app.route('/match/pending', methods=['GET'])
def router_pending_matches():
    conn = create_conn(path)
    userid = request.args.get('userid')
    ja = get_pending_matches(conn, userid)
    kill_conn(conn)
    return response(Match.RECEIVED, ja)


@app.route('/match/confirm', methods=['POST'])
def router_confirm_match():
    conn = create_conn(path)
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    if login(conn, username, passwd) is Login.SUCCESSFUL:
        for match in json.loads(request.form.get('matches')):
            print(match.get('matchid'))
            if match.get('confirmed') is True:
                matchid = match.get('matchid')
                r = confirm_match(conn, matchid)
                remove_pending_match(conn, matchid)
        kill_conn(conn)
        return response(r)
    else:
        return "error"


@app.route('/leaderboard', methods=['GET'])
def router_leaderboard():
    conn = create_conn(path)
    l = leaderboard(conn).fetchall()
    arr = []
    for entry in l:
        username = entry[0]
        elo = entry[1]
        arr.append({"username": username, "elo": elo})
    kill_conn(conn)
    return response(Leaderboard.FINE, arr)
