from werkzeug.wrappers import Request, Response, ResponseStream

import config
import validate
import response_new
import security
import connection


class middleware():

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        request = Request(environ)

        # create database connection
        conn = connection.create(config.database)

        device_version = request.headers.get('version')
        ip = request.remote_addr

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
            res = response_new.build({"outdated_app_version": True,
                                      "status": "Du benutzt eine veraltete App Version. Bitte lade die neuste Version "
                                                "herunter um BeerKing weiter nutzen zu können. GutTrink du Saufnase!"
                                      }, statuscode=403)
            return res(environ, start_response)

        # ip banned
        if security.ip_is_banned(conn, ip):
            res = response_new.build({"status": "banned"}, statuscode=401)
            return res(environ, start_response)

        # user banned
        if security.user_is_banned(conn, username, ip=ip):
            res = response_new.build({"status": "banned"}, statuscode=401)
            return res(environ, start_response)

        # sql injection
        if security.is_no_sql_injection(arr, request.remote_addr):
            res = response_new.build({"status": "banned"}, statuscode=401)
            return res(environ, start_response)

        # rdp
        if security.is_no_rdp_attempt(request, request.remote_addr):
            res = response_new.build({"status": "banned"}, statuscode=401)
            return res(environ, start_response)

        # middleware passed
        return self.app(environ, start_response)
