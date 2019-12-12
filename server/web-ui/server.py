import flask
import json
from flask_cors import CORS
from flask import Flask, render_template, send_from_directory, Response

CORS(app)
app = Flask(__name__, template_folder="./beerking/www/", static_folder="./beerking/www/css")


@app.route('/status', methods=["GET"])
def router_status():
    resp = Response(json.dumps({"status": "available"}), mimetype='application/json', status=200)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route('/beerking', methods=['GET'])
def _base_redirect():
    """ Redirect help handler"""
    return flask.redirect("/beerking/index.html")


@app.route('/beerking/<file>', methods=['GET'])
def base_html(file):
    """ Documentation handler"""
    if ".html" in file:
        return render_template(file)
    if ".js" in file:
        return send_from_directory("beerking/www", file)


@app.route('/beerking/<path>/<file>', methods=['GET'])
def static_files(path, file):
    return send_from_directory("beerking/www/" + path, file)


@app.route('/beerking/plugins/<plug>/<folder>/<file>', methods=['GET'])
def plugins(plug, folder, file):
    return send_from_directory("beerking/www/plugins/" + plug + "/" + folder, file)


@app.route('/beerking/plugins/<plug>/<folder>/<browser>/<file>', methods=['GET'])
def plugins_long(plug, folder, browser, file):
    return send_from_directory("beerking/www/plugins/" + plug + "/" + folder + "/" + browser, file)
