###############################################################################
#
#   Copyright (C) 2021 ACSONE SA/NV (http://www.acsone.eu).
#   @author Laurent Mignon <laurent.mignon@acsone.eu>
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

import re
import threading

import serial
from flask import jsonify

from pywebdriver import app, config

values = {}


@app.before_first_request
def activate_job():
    read_thread = threading.Thread(target=serrial_reader_task)
    read_thread.daemon = True
    read_thread.start()


def serrial_reader_task():
    ser = serial.Serial(
        port=config.get("mettler_toledo_driver", "port") or "/dev/ttyS0",
        baudrate=config.getint("mettler_toledo_driver", "baudrate") or 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0,
    )
    buffer = ""
    ser.read()
    global values
    while True:
        line = ser.readline()
        try:
            buffer += line.decode("utf-8")
        except UnicodeDecodeError:
            buffer = ""
            continue
        try:
            pos = buffer.index("\r\n")
        except ValueError:
            continue
        buffer = buffer[:pos]
        matches = re.match(
            r"^S (?P<stability>[SD])  (?P<weight> +([0-9\.]+)) kg$",
            buffer[:pos],
        )
        if matches:
            buffer = ""
            groups = matches.groupdict()
            stability = groups["stability"]
            value = float(groups["weight"])
            status = "FIXED" if stability == "S" else "ACQUIRING"
            values.update({"value": value, "status": status})


@app.route("/hw_proxy/weight", methods=["GET"])
def serial_read_http():
    return jsonify(**values)

