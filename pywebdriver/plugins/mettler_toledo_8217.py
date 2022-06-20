# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import logging
import re

import serial

from .scale_driver import AbstractScaleDriver

ANSWER_RE = re.compile(rb"^\?(?P<status>.)|(?P<weight>\d+\.\d+)$")

_logger = logging.getLogger(__name__)


class MettlerToledo8217ScaleDriver(AbstractScaleDriver):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.vendor_product = "mettler_toledo_8217"

    @property
    def _port(self):
        return self.config.get("scale_driver", "port", fallback="/dev/ttyS0")

    @property
    def _baudrate(self):
        return self.config.getint("scale_driver", "baudrate", fallback=9600)

    @property
    def weight(self):
        """Return the last reported weight of the scale."""
        with self.data_lock:
            return self.data.get("value", 0)

    @property
    def scale_status(self):
        """Return the last reported status of the scale."""
        with self.data_lock:
            return self.data.get("status", "ERROR")

    def acquire_data(self, connection):
        """Acquire data over the connection."""
        buffer = b""
        stx = False
        # ask for weight data
        connection.write(b"W")
        while True:
            c = connection.read(1)
            if not c:
                # timeout
                raise serial.SerialTimeoutException()
            if c == b"\x02":
                # start of answer
                stx = True
                buffer = b""
            elif c == b"\r":
                # end of answer
                if not stx:
                    continue
                break
            else:
                buffer += c
        match = ANSWER_RE.match(buffer)
        if match is None:
            raise ValueError("serial readout was not valid")
        matchdict = match.groupdict()
        _logger.debug(matchdict)
        status = matchdict["status"]
        weight = matchdict["weight"]
        result = self.data.copy()
        if weight is not None:
            result.update({"value": float(weight), "status": "FIXED"})
            return result
        if not isinstance(status, bytes):
            return result
        status_byte = int.from_bytes(status, byteorder="big")
        if status_byte & 0b1:
            # in motion
            result.update({"status": "ACQUIRING"})
        elif status_byte & 0b110:
            result.update({"status": "ERROR"})
        return result

    def establish_connection(self):
        """Establish a connection. The connection must be a context manager."""
        return serial.Serial(
            port=self._port,
            baudrate=self._baudrate,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS,
            timeout=1,
        )

    def is_connection_active(self, connection):
        """Ascertain whether the connection is active and healthy."""
        if not connection or not connection.isOpen():
            return False
        try:
            connection.read(1)
        except serial.SerialException:
            return False
        return True
