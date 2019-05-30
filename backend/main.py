from flask import Flask
from flask import request
import sqlite3
import uuid as uuid_helper
import hashlib
app = Flask(__name__)

@app.route('/users/creation')
def user_creation():
    try:
        uuid = str(uuid_helper.uuid4())
        username = request.args.get('username')
        mail = request.args.get('email')
        passwd = hashlib.sha512(str(request.args.get('passwd')).encode()).hexdigest()
        conn = sqlite3.connect('/root/beerpong/beerpong.db')
        c = conn.cursor()
        c.execute("""INSERT INTO users(uuid, username, email, passwd) 
            VALUES (?,?,?,?);""", (str(uuid), str(username), str(mail), str(passwd)))
        conn.commit()
        conn.close()
    except:
        pass
    return 'user created.<br>uuid: ' + str(uuid) + '<br>username: ' + str(username) + '<br>email: ' + str(mail)