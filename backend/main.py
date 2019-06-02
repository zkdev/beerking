from flask import Flask
from flask import request
from .generator.generate_uuid import main as uuid4
from .connection.create import main as create_conn
from .connection.kill import main as kill_conn
from .handlers.create_user.main import main as create_user
from .handlers.login.main import main as login


app = Flask(__name__)


@app.route('/users/creation', methods=['POST'])
def user_creation():
    conn = create_conn('/root/beerpong/beerpong.db')
    uuid = uuid4(conn)
    username = request.args.get('username')
    mail = request.args.get('mail')
    passwd = str(request.args.get('passwd')).lower()
    r = create_user(conn, uuid, username, mail, passwd)
    kill_conn(conn)
    return r


@app.route('/users/login', methods=['GET'])
def user_login():
    conn = create_conn('/root/beerpong/beerpong.db')
    username = request.args.get('username')
    passwd = str(request.args.get('passwd')).lower()
    r = login(conn, username, passwd)
    kill_conn(conn)
    return r




