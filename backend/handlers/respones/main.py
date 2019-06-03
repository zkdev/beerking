from flask import Response
from ...enums.enums import Login, Create


def main(enum):
    resp = Response(mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'

    if enum is Create.SUCCESSFUL:
        # POST
        # 201 = Created
        resp.status_code = 201
        resp = "{'status':'user creation successful'}"
    elif enum is Create.USERNAME_NOT_UNIQUE:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        resp = "{'status':'user creation failed, username is not unique'}"
    elif enum is Create.USERNAME_DOESNT_MATCH_REQUIREMENTS:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        resp = "{'status':'user creation failed, username doesn't match requirements'}"
    elif enum is Create.MAIL_NOT_EXISTING:
        # POST
        # 400 = Bad Request
        resp.status_code = 400
        resp = "{'status':'user creation failed, mail doesn't exist'}"
    elif enum is Login.SUCCESSFUL:
        # GET
        # 200 = OK
        resp.status_code = 200
        resp = "{'status':'login successful'}"
    elif enum is Login.USERNAME_NOT_FOUND:
        # GET
        # 403 = Forbidden
        resp.status_code = 403
        resp = "{'status':'login failed, username not found'}"
    elif enum is Login.PASSWD_WRONG:
        # GET
        # 403 = Forbidden
        resp.status_code = 403
        resp = "{'status':'login failed, passwd rejected'}"
    else:
        # DEFAULT
        # 500 = Internal Server Error
        resp.status_code = 500

    return resp
