from flask import Flask
from flask import request
from flask_cors import CORS
from .generator.generate_uuid import main as uuid4
from .connection.create import main as create_conn
from .connection.kill import main as kill_conn
from .handlers.create_user.main import main as create_user
from .handlers.login.main import main as login
from .handlers.respones.main import main as response
from .match import start_1v1, start_2v2
from .handlers.profile.main import main as profile


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


@app.route('/match/start/1v1', methods=['POST'])
def router_start_1v1():
    conn = create_conn(path)
    host = request.form.get('host')
    enemy = request.form.get('enemy')
    r = start_1v1(conn, host, enemy)
    kill_conn(conn)
    return response(r)


@app.route('/match/start/2v2', methods=['POST'])
def router_start_2v2():
    conn = create_conn(path)
    host = request.form.get('host')
    friend = request.form.get('friend')
    enemy1 = request.form.get('enemy1')
    enemy2 = request.form.get('enemy2')
    r = start_2v2(conn, host, friend, enemy1, enemy2)
    kill_conn(conn)
    return response(r)
