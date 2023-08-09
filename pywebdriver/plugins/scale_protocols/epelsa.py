""""
 Epelsa Scale answer format:
  * initial weight: \x02I  0.000\r\x03
  * stable weight: \x02A -0.450\r\x03
  * transition weight: \x02! -0.250\r\x03
"""

import re

import serial

from ..scale_driver import (
    AbstractScaleDriver,
    ScaleAcquireDataError,
    ScaleConnectionError,
)

measureRegexp = re.compile(b"[A-Z]\\s*(-?[0-9.]+)\r")


class EpelsaScaleDriver(AbstractScaleDriver):
    """Driver for the Epelsa protocol configured in Auto mode."""

    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.vendor_product = "epelsa"
        self._poll_interval = self.config.getfloat(
            "scale_driver", "poll_interval", fallback=0.2
        )
        self._last_weight = 0.0

    @property
    def poll_interval(self):
        return self._poll_interval

    @property
    def _port(self):
        return self.config.get("scale_driver", "port", fallback="/dev/ttyUSB0")

    @property
    def _baudrate(self):
        return self.config.getint("scale_driver", "baudrate", fallback=9600)

    def acquire_data(self, connection):
        buffer = self._read_raw_data(connection)
        match = measureRegexp.match(buffer)
        if match:
            weight = float(match.group(1))
            if weight is not None:
                self._last_weight = float(weight)
        return {
            "value": self._last_weight,
            "status": self.VALID_WEIGHT_STATUS,
        }

    def _read_raw_data(self, connection):
        answer = []
        char = ""
        stx = False

        while True:
            try:
                char = connection.read(1)
            except serial.SerialException as e:
                raise ScaleConnectionError() from e
            if not char:
                # timeout
                raise ScaleAcquireDataError("read time-out")
            if char == b"\x02":
                # start of answer
                stx = True
                answer = b""
            elif char == b"\x03" and stx:
                # end of answer
                break
            else:
                answer += char
        connection.reset_input_buffer()
        return answer

    def establish_connection(self):
        return serial.Serial(
            port=self._port,
            baudrate=self._baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
