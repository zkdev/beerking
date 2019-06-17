import json

from flask import Response
from .enums import Auth, User, Match, Version, Leaderboard, History, Friends, Reason


def build(enum, rs=None):
    resp = Response(mimetype='application/json')
    resp.headers.add('Access-Control-Allow-Origin', '*')
    server_message = "This version is under development and might be unstable."

    if enum is Auth.SUCCESSFUL:
        userid, mail = rs[0]
        resp.status_code = 200
        json_obj = {"auth": True, "userid": userid, "mail": mail, "server_message": server_message}
    elif enum is Auth.FAILED:
        resp.status_code = 401
        json_obj = {"auth": False, "server_message": server_message}
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
        json_obj = {"user_created": False, "username_unique": True}
    elif enum is Reason.USERNAME_NOT_UNIQUE:
        resp.status_code = 400
        json_obj = {"user_created": False, "username_unique": False}
    elif enum is Reason.USERNAME_TOO_SHORT:
        resp.status_code = 400
        json_obj = {"user_created": False, "username_too_short": True}
    elif enum is Reason.MAIL_DOESNT_EXIST:
        resp.status_code = 400
        json_obj = {"user_created": False, "mail_exists": False}
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
        json_obj = {"matches_confirmed": True}
    elif enum is Match.RECEIVED:
        resp.status_code = 200
        json_obj = {"matches_received": True, "matches": rs}
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
    elif enum is User.ID_EXISTS:
        resp.status_code = 200
        json_obj = {"userid_exists": True}
    elif enum is User.ID_DOESNT_EXIST:
        resp.status_code = 401
        json_obj = {"userid_exists": False}
    elif enum is Friends.RETRIEVED:
        resp.status_code = 200
        arr = []
        for entry in rs:
            friendname, friendid = entry
            arr.append({"friend": friendid, "friendname": friendname})
        json_obj = {"friends": arr}
    elif enum is Friends.ADDED:
        resp.status_code = 201
        json_obj = {"friend_added": True}
    elif enum is Friends.REMOVED:
        resp.status_code = 200
        json_obj = {"friend_removed": True}
    elif enum is Reason.FRIENDS_ALREADY:
        resp.status_code = 400
        json_obj = {"friend_added": False, "friends_already": True}
    elif enum is Reason.FRIEND_DOESNT_EXIST:
        resp.status_code = 400
        json_obj = {"friend_added": False, "friend_doesnt_exist": True}
    elif enum is Reason.SAME_AS_USER:
        resp.status_code = 400
        json_obj = {"friend_added": False, "friend_equal_user": True}
    else:
        resp.status_code = 500

    resp = json.dumps(json_obj)
    return resp
