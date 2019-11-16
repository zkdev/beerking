import config
import json
from flask import Response


def build(json_obj, statuscode=500):
    resp = Response(json.dumps(json_obj), mimetype='application/json', status=statuscode)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add("Backend-Mode", config.backend_mode)
    return resp
