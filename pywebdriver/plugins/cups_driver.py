# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64
import logging
import tempfile

import cups
from flask import jsonify, make_response, request

from pywebdriver import app, drivers

from .base_driver import AbstractDriver

_logger = logging.getLogger(__name__)


class ExtendedCups(cups.Connection):
    def printData(self, printer, data, title="Pywebdriver", options=None):
        with tempfile.NamedTemporaryFile() as f:
            f.write(base64.b64decode(data))
            f.flush()
            res = self.printFile(printer, f.name, title, options)
        return res

    def printFile(self, printer, filename, title="Pywebdriver", options=None):
        if options is None:
            options = {}
        string_options = {}
        for key, value in options.items():
            string_options[str(key)] = str(value)
        return super(ExtendedCups, self).printFile(
            printer, filename, title, string_options
        )

    def printFiles(self, printer, filenames, title="Pywebdriver", options=None):
        if options is None:
            options = {}
        string_options = {}
        for key, value in options.items():
            string_options[str(key)] = str(value)
        return super(ExtendedCups, self).printFiles(
            printer, filenames, title, string_options
        )


class CupsDriver(AbstractDriver):
    def getConnection(self):
        try:
            return ExtendedCups()
        except BaseException:
            return False

    def get_vendor_product(self):
        return "cups-icon"

    def get_status(self, **params):
        messages = []
        mapstate = {
            3: "Idle",
            4: "Printing",
            5: "Stopped",
        }
        conn = self.getConnection()
        if not conn:
            return {
                "status": "disconnected",
                "messages": ["Cups Sever is not running"],
            }
        for printer, value in self.getConnection().getPrinters().items():
            messages.append("{} : {}".format(printer, mapstate[value["printer-state"]]))
        state = {
            "status": "connected",
            "messages": messages,
        }
        return state


@app.route("/cups/printData", methods=["POST", "GET", "PUT"])
@app.route("/printers/printData", methods=["POST", "GET", "PUT"])
def printersapi():
    args = []
    kwargs = {}
    if request.json:
        args = request.json.get("args", [])
        kwargs = request.json.get("kwargs", {})
    if request.args:
        kwargs = request.args.to_dict()
    conn = drivers["cups"].getConnection()
    try:
        result = conn.printData(*args, **kwargs)
    # TODO we should implement all cups error
    except cups.IPPError as e:
        err = str(e)
        return make_response(
            jsonify(
                {
                    "cups_error": "IPPError",
                    "cups_error_status": err,
                    "cups_error_description": err,
                }
            ),
            400,
        )

    return jsonify(jsonrpc="2.0", result=result)


drivers["cups"] = CupsDriver()
