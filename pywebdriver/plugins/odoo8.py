# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from flask import jsonify, make_response, request

from pywebdriver import app, drivers


@app.route("/hw_proxy/hello", methods=["GET"])
def hello_http():
    return make_response("ping")


@app.route("/hw_proxy/handshake", methods=["POST", "GET", "PUT"])
def handshake_json():
    return jsonify(jsonrpc="2.0", result=True)


@app.route("/hw_proxy/status_json", methods=["POST", "GET", "PUT"])
def status_json():
    statuses = {}
    params = request.json["params"]
    for driver in drivers:
        statuses[driver] = drivers[driver].get_status(**params)
    return jsonify(jsonrpc="2.0", result=statuses)


@app.route("/hw_proxy/log", methods=["POST", "GET", "PUT"])
def log_json():
    arguments = request.json["params"]["arguments"]
    print(" ".join(str(v) for v in arguments))
    return jsonify(jsonrpc="2.0", result=True)
