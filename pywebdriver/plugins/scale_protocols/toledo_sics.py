# Copyright (C) 2022-Today Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
import re
import serial

from ..scale_driver import (
    AbstractScaleDriver,
    ScaleAcquireDataError,
    ScaleConnectionError,
)

_logger = logging.getLogger(__name__)

# Example: "S S    125.67 g"
SICS_ANSWER_RE = re.compile(rb"^S\s\S\s+(?P<weight>[-+]?\d+\.\d+)\s*g")

class MTSICSScaleDriver(AbstractScaleDriver):
    """Driver for Mettler-Toledo MT-SICS protocol"""

    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.vendor_product = "toledo_sics"
        self._poll_interval = self.config.getfloat(
            "scale_driver", "poll_interval", fallback=0.5
        )
        self._last_weight = 0.0

    @property
    def poll_interval(self):
        return self._poll_interval

    @property
    def _port(self):
        return self.config.get("scale_driver", "port", fallback="/dev/ttyS0")

    @property
    def _baudrate(self):
        return self.config.getint("scale_driver", "baudrate", fallback=9600)

    def acquire_data(self, connection):
        """Acquire weight data from MT-SICS scale using SI command"""
        try:
            connection.write(b"SI\r\n")
        except serial.SerialException as e:
            raise ScaleConnectionError() from e

        try:
            response = connection.readline()
        except serial.SerialException as e:
            raise ScaleAcquireDataError("read failed") from e

        _logger.debug(f"SICS raw response: {response!r}")

        match = SICS_ANSWER_RE.match(response)
        if not match:
            raise ScaleAcquireDataError("Unexpected SICS format: ", response)

        weight = float(match.group("weight"))
        self._last_weight = weight

        return {
            "value": weight,
            "status": self.VALID_WEIGHT_STATUS,
        }

    def establish_connection(self):
        """Establish and return serial connection to scale"""
        return serial.Serial(
            port=self._port,
            baudrate=self._baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
