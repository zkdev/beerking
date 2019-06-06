import json

from flask import Response
from ...enums.enums import Login, Create, Match


def main(enum, p=None):
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
        userid, mail = p[0]
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
    elif enum is Match.PENDING:
        # POST
        # 201 = Created
        resp.status_code = 201
        json_obj = {"status": "match start successful"}
    else:
        # DEFAULT
        # 500 = Internal Server Error
        resp.status_code = 500

    resp = json.dumps(json_obj)
    return resp
