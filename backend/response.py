import json

from flask import Response
from .enums import Login, User, Match, Version, Leaderboard, History


def build(enum, rs=None):
    resp = Response(mimetype='application/json')
    resp.headers.add('Access-Control-Allow-Origin', '*')

    if enum is Login.SUCCESSFUL:
        userid, mail = rs[0]
        resp.status_code = 200
        json_obj = {"auth": True, "userid": userid, "mail": mail}
    elif enum is Login.FAILED:
        resp.status_code = 401
        json_obj = {"auth": False}
    elif enum is User.MAIL_UPDATED:
        resp.status_code = 202
        json_obj = {"mail_updated": True}
    elif enum is User.MAIL_UPDATE_FAILED:
        resp.status_code = 403
        json_obj = {"mail_updated": False}
    elif enum is User.CREATED:
        resp.status_code = 201
        json_obj = {"user_created": True}
    elif enum is User.NOT_CREATED:
        resp.status_code = 400
        json_obj = {"user_created": False}
    elif enum is Match.STARTED:
        resp.status_code = 201
        json_obj = {"match_started": True}
    elif enum is Match.NOT_STARTED:
        resp.status_code = 400
        json_obj = {"match_started": False}
    elif enum is Version.OUTDATED:
        resp.status_code = 403
        json_obj = {"outdated_app_version": True}
    elif enum is Match.CONFIRMED:
        resp.status_code = 201
        json_obj = {"match_confirmed": True}
    elif enum is Match.RECEIVED:
        resp.status_code = 200
        json_obj = {"match_received": True, "matches": rs}
    elif enum is Leaderboard.RETRIEVED:
        resp.status_code = 200
        return json.dumps({"leaderboard": rs})
    elif enum is History.RETRIEVED:
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

    """
    elif enum is Match.CONFIRMED:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "match confirmed"}
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
    elif enum is Friends.FINE:
        # GET
        # 200 = OK
        resp.status_code = 200
        arr = []
        for entry in rs:
            friendname, friendid = entry
            arr.append({"friend": friendid, "friendname": friendname})
        json_obj = {"friends": arr}
    elif enum is Friends.ADDED:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "friend added"}
    elif enum is Friends.REMOVED:
        # DELETE
        # 200 = OK
        resp.status_code = 200
        json_obj = {"status": "friend removed"}
    else:
        # DEFAULT
        # 500 = Internal Server Error
        resp.status_code = 500"""

    resp = json.dumps(json_obj)
    return resp
