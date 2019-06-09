import json

from flask import Response
from .enums import Login, Create, Match, Leaderboard


def build(enum, rs=None):
    resp = Response(mimetype='application/json')
    resp.headers.add('Access-Control-Allow-Origin', '*')

    if enum is Create.SUCCESSFUL:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "user creation successful"}
    elif enum is Create.USERNAME_NOT_UNIQUE:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        json_obj = {"status": "user creation failed, username is not unique"}
    elif enum is Create.USERNAME_DOESNT_MATCH_REQUIREMENTS:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        json_obj = {"status": "user creation failed, username doesn't match requirements"}
    elif enum is Create.MAIL_NOT_EXISTING:
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
    else:
        # DEFAULT
        # 500 = Internal Server Error
        resp.status_code = 500

    resp = json.dumps(json_obj)
    return resp
