from werkzeug.wrappers import Request, Response, ResponseStream

import config
import validate
import response
import security
import connection


class middleware():

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        request = Request(environ)

        # ignore options call
        if request.method == "OPTIONS":
            return self.app(environ, start_response)

        # create database connection
        conn = connection.create(config.database)

        device_version = request.headers.get('version')
        ip = request.remote_addr

        username = ""
        arr = []

        # POST
        if request.method == "POST":
            username = request.form.get('username')
            mail = request.form.get('mail')
            passwd = request.form.get('passwd')
            arr = [ip, username, mail, passwd]

        # GET
        elif request.method == "GET":
            username = request.args.get('username')
            mail = request.args.get('mail')
            passwd = request.args.get('passwd')
            arr = [ip, username, mail, passwd]

        # version
        if not validate.is_correct_version(device_version):
            res = response.build({"outdated_app_version": True}, statuscode=403)
            print("version outdated", flush=True)
            return res(environ, start_response)

        # empty auth
        if validate.catch_empty_auth(username, passwd):
            return response.build({"auth": False}, statuscode=401)

        # ip banned
        if security.ip_is_banned(conn, ip):
            res = response.build({"status": "banned"}, statuscode=401)
            print("ip banned", flush=True)
            return res(environ, start_response)

        # user banned
        if security.user_is_banned(conn, username, ip=ip):
            res = response.build({"status": "banned"}, statuscode=401)
            print("user banned", flush=True)
            return res(environ, start_response)

        # sql injection
        if not security.is_no_sql_injection(arr, request.remote_addr):
            res = response.build({"status": "banned"}, statuscode=401)
            print("sql injection", flush=True)
            return res(environ, start_response)

        # rdp
        if not security.is_no_rdp_attempt(request, request.remote_addr):
            res = response.build({"status": "banned"}, statuscode=401)
            print("rdp attempt", flush=True)
            return res(environ, start_response)

        # middleware passed
        return self.app(environ, start_response)
