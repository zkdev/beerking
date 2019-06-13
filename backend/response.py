import json

from flask import Response
from .enums import Login, Create, Match, Leaderboard, Profile, History, Id, Mail, Friends


def build(enum, rs=None):
    resp = Response(mimetype='application/json')
    resp.headers.add('Access-Control-Allow-Origin', '*')

    if enum is Create.ERFOLGREICH:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "user creation successful"}
    elif enum is Create.NUTZERNAME_EXISTIERT_BEREITS:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        json_obj = {"status": "user creation failed, username is not unique"}
    elif enum is Create.NUTZERNAME_ERFUELLT_BEDINGUNGEN_NICHT:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        json_obj = {"status": "user creation failed, username doesn't match requirements"}
    elif enum is Create.MAIL_EXISTIERT_NICHT:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        json_obj = {"status": "user creation failed, mail doesn't exist"}
    elif enum is Login.SUCCESSFUL:
        # GET
        # 200 = OK
        userid, mail = rs[0]
        resp.status_code = 200
        json_obj = {"status": "login successful", "userid": userid, "mail": mail}
    elif enum is Login.USERNAME_NOT_FOUND:
        # GET
        # 403 = Forbidden
        resp.status_code = 403
        json_obj = {"status": "login failed, username not found"}
    elif enum is Login.PASSWD_WRONG:
        # GET
        # 403 = Forbidden
        resp.status_code = 403
        json_obj = {"status": "login failed, passwd rejected"}
    elif enum is Match.FINE:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "match created successful"}
    elif enum is Match.RECEIVED:
        # GET
        # 200 = OK
        return json.dumps({"matches": rs})
    elif enum is Match.CONFIRMED:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "match confirmed"}
    elif enum is Leaderboard.FINE:
        # GET
        # 200 = OK
        resp.status_code = 200
        return json.dumps({"leaderboard": rs})
    elif enum is Profile.UPDATED:
        # PUT
        # 202 = Accepted
        resp.status_code = 202
        json_obj = {"status": "mail updated"}
    elif enum is History.FINE:
        # GET
        # 200 = OK
        arr = []
        for entry in rs:
            host = entry[0]
            friend = entry[1]
            enemy1 = entry[2]
            enemy2 = entry[3]
            winner = entry[4]
            date_data = entry[5]
            arr.append({"host": host, "friend": friend, "enemy1": enemy1, "enemy2": enemy2, "winner": winner, "datetime": date_data})
        return json.dumps({"matches": arr})
    elif enum is Id.EXISTS:
        # GET
        # 200 = OK
        resp.status_code = 200
        json_obj = {"status": "userid exists"}
    elif enum is Id.DOESNT_EXIST:
        # GET
        # 403 = Forbidden
        resp.status_code = 403
        json_obj = {"status": "userid doesnt exists"}
    elif enum is Mail.NOT_EXISTING:
        # PUT
        # 403 = Forbidden
        resp.status_code = 403
        json_obj = {"status": "mail update failed, mail not exisiting"}
    elif enum is Friends.FINE:
        # GET
        # 200 = OK
        return json.dumps({"friends": rs})
    elif enum is Friends.ADDED:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "friend added"}
    else:
        # DEFAULT
        # 500 = Internal Server Error
        resp.status_code = 500

    resp = json.dumps(json_obj)
    return resp
