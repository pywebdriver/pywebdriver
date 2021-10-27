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

import logging
import re
import threading
from contextlib import closing

import serial
from flask import jsonify

from pywebdriver import app, config

values = {}
read_thread = None

_logger = logging.getLogger(__name__)


def serial_connect():
    return serial.Serial(
        port=config.get("mettler_toledo_driver", "port") or "/dev/ttyS0",
        baudrate=config.getint("mettler_toledo_driver", "baudrate") or 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0,
    )


def serial_reader_task():
    global values
    try:
        ser = serial_connect()
        with closing(ser):
            buffer = ""
            ser.read()
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
                    r"^S (?P<stability>[SD])( )*(?P<weight>(-)?([0-9\.]+))( )*kg",
                    buffer[:pos],
                )
                if matches:
                    buffer = ""
                    groups = matches.groupdict()
                    stability = groups["stability"]
                    value = float(groups["weight"])
                    status = "FIXED" if stability == "S" else "ACQUIRING"
                    values.update({"value": value, "status": status})
                elif "kg" in buffer or len(buffer) > 128:
                    # reset buffer we maybe have a partial value into the buffer
                    buffer = ""
    except Exception as e:
        _logger.exception("Unable to get data from serial")
        values.update({"value": str(e), "status": "ERROR"})
        raise e


@app.before_first_request
def start_read_thread_job():
    global read_thread
    read_thread = threading.Thread(target=serial_reader_task)
    read_thread.daemon = True
    read_thread.start()


@app.before_request
def check_read_thread_alive_job():
    global read_thread
    if not read_thread or not read_thread.is_alive():
        start_read_thread_job()


@app.route("/hw_proxy/weight", methods=["GET"])
def serial_read_http():
    return jsonify(**values)
