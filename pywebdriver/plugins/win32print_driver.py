# Copyright 2020 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import logging
import os
import tempfile

from flask import jsonify, make_response, request

from pywebdriver import app, drivers

from .base_driver import AbstractDriver

_logger = logging.getLogger(__name__)

try:  # noqa: C901
    import win32api
    import win32print
except ImportError:
    installed = False
    print("WIN32: win32print python library not installed")
else:

    class Win32printDriver(AbstractDriver):
        def get_vendor_product(self):
            return "windows-icon"

        def get_status(self, **params):
            messages = []
            for printer in win32print.EnumPrinters(
                win32print.PRINTER_ENUM_NAME, None, 5
            ):
                messages.append(printer["pPrinterName"])
            state = {
                "status": "connected",
                "messages": messages,
            }
            return state

        def printData(self, printer, data, title="Pywebdriver", options=None):
            if options and options.get("raw"):
                copies = options.get("copies") or 1
                i = 0
                while i < copies:
                    res = self.printRaw(printer, data, title)
                    i = i + 1
                    if res != 0:
                        return res
                return 0
            else:
                return self.printPdf(printer, data)

        def printRaw(self, printer, data, title):
            hPrinter = win32print.OpenPrinter(printer)
            try:
                win32print.StartDocPrinter(hPrinter, 1, (title, None, "RAW"))
                try:
                    win32print.StartPagePrinter(hPrinter)
                    win32print.WritePrinter(hPrinter, base64.b64decode(data))
                    win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
            return 0

        def printPdf(self, printer, data):
            defaultPrinter = win32print.GetDefaultPrinter()
            win32print.SetDefaultPrinter(printer)
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                f.write(base64.b64decode(data))
                f.flush()
                filename = os.path.basename(f.name)
                dirname = os.path.dirname(f.name)
                win32api.ShellExecute(0, "print", filename, None, dirname, 0)
            win32print.SetDefaultPrinter(defaultPrinter)
            return 0

    drivers["win32print"] = Win32printDriver()

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
        driver = drivers["win32print"]
        try:
            result = driver.printData(*args, **kwargs)
        # TODO we should implement all cups error
        except Exception as e:
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
