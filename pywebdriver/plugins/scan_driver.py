###############################################################################
#
#   Copyright (C) 2021 KMEE (http://www.kmee.com.br).
#   @author Luis Felipe Mileo <mileo@kmee.com.br>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import glob
import os
import sys

import serial
from flask import jsonify
from serial.tools import list_ports

from pywebdriver import app, config, drivers

from .base_driver import AbstractDriver


class MagneticStripeReader:
    def __init__(self, port=False):
        values = dict()
        values["port"] = port or os.environ.get("IOT_SCAN_PORT", "/dev/ttyS0")
        values["baudrate"] = config.getint("scan_driver", "baudrate")
        values["bytesize"] = config.getint("scan_driver", "bytesize")
        values["parity"] = config.get("scan_driver", "parity")
        values["stopbits"] = config.getint("scan_driver", "stopbits")
        values["rtscts"] = config.getboolean("scan_driver", "rtscts")
        values["xonxoff"] = config.getboolean("scan_driver", "xonxoff")
        values["timeout"] = None
        values["eol_cr"] = config.getboolean("scan_driver", "eol_cr")
        values["eol_lf"] = config.getboolean("scan_driver", "eol_lf")

        port = values["port"]
        app.logger.debug(f"scan port {port}")

        if (
            sys.platform.startswith("linux")
            or sys.platform.startswith("cygwin")
            or sys.platform.startswith("darwin")
        ):
            if not port.startswith("/dev/tty"):
                raise serial.SerialException("%s: invalid serial port" % port)

        app.logger.debug("serial: open %r", values)
        self._serial = serial.Serial(
            port=values["port"],
            baudrate=values["baudrate"],
            bytesize=values["bytesize"],
            parity=values["parity"],
            stopbits=values["stopbits"],
            rtscts=values["rtscts"],
            xonxoff=values["xonxoff"],
            timeout=values["timeout"],
        )

    def scan_close(self):
        if self._serial:
            self._serial.close()

    def _read_data_in_waiting(self):
        read_buffer = b""
        for read in self._serial.iread_until(expected=serial.CR):
            read_buffer += read
            if not self._serial.inWaiting():
                break
        return read_buffer.decode("utf-8").replace("\r", "")

    def scan_do_operation(self, operation):
        result = {}
        try:
            if self._serial:
                if operation == "read":
                    result["data"] = self._read_data_in_waiting()
                result["status"] = "ok"
        except serial.SerialException as message:
            result["status"] = "error"
            result["message"] = str(message)
        self.scan_close()

        return result


class ScannerDriver(AbstractDriver):
    def getConnection(self):
        try:
            return MagneticStripeReader()
        except BaseException as e:
            app.logger.error(e)
            return False

    def discover(self):
        tty = glob.glob("/dev/ttyS*")
        tty += glob.glob("/dev/ttyX*")
        tty += glob.glob("/dev/ttyACM*")
        connection = []
        for port in tty:
            try:
                connection.append(port)
            except BaseException as e:
                app.logger.error(e)
                continue
        return connection

    def get_vendor_product(self):
        return "scanner-icon"

    def get_status(self, **params):
        messages = []
        conn = self.getConnection()
        if not conn:
            return {
                "status": "disconnected",
                "messages": ["Scanner disconnected"],
            }

        ports = list_ports.comports()

        for port, desc, hwid in sorted(ports):
            messages.append("{}: {} [{}]".format(port, desc, hwid))
        state = {
            "status": "connected",
            "messages": messages,
        }
        return state


@app.route("/hw_proxy/scanner", methods=["POST"])
def scan_scan_http():
    conn = drivers["scanner"].getConnection()
    result = conn.scan_do_operation("read")
    barcode = result.get("data")
    return jsonify(jsonrpc="2.0", result=barcode)


@app.route("/hw_proxy/scanner_discover", methods=["POST"])
def scanner_discover_http():
    conn = drivers["scanner"].discover()
    return jsonify(jsonrpc="2.0", result=conn)


drivers["scanner"] = ScannerDriver()
