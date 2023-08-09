# Copyright (C) 2022-Today Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
import time
from abc import ABC, abstractmethod
from contextlib import ExitStack
from importlib import import_module
from threading import RLock, Thread

from flask import jsonify

from pywebdriver import app, config, drivers

from .base_driver import AbstractDriver

_logger = logging.getLogger(__name__)

driver = None

WEIGHT_UNIT_TO_KG = {
    "kg": 1,
    "g": 0.001,
    "lb": 0.45359237,
    "oz": 0.02834952,
}


class ScaleError(Exception):
    """Base exception."""


class ScaleConnectionError(ScaleError):
    """Raised when the connection with the scale is not healthy when trying to
    acquire data from it.
    """


class ScaleAcquireDataError(ScaleError):
    """An error occurred during the acquiring of data that did not break the
    connection.
    """


class AbstractScaleDriver(Thread, AbstractDriver, ABC):
    VALID_WEIGHT_STATUS = "ok"

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, daemon=True, **kwargs)

        self.active = False
        self.config = config
        self.connection = None
        self._data = {}
        self._data_lock = RLock()
        self.vendor_product = "default_scale"

        weight_unit = config.get("scale_driver", "unit", fallback="kg")
        self.kg_per_unit = WEIGHT_UNIT_TO_KG.get(weight_unit)
        if self.kg_per_unit is None:
            raise ValueError("unsupported scale unit: {unit}".format(unit=weight_unit))

    @property
    def weight(self):
        """Return the last reported weight of the scale in kg."""
        with self._data_lock:
            value = self._data.get("value")
            if value is not None:
                value *= self.kg_per_unit
            return value

    @property
    def scale_status(self):
        """Return the last reported status of the scale."""
        with self._data_lock:
            return self._data.get("status", ["error"])

    @property
    @abstractmethod
    def poll_interval(self):
        """Time between polls to the scale."""

    def get_vendor_product(self):
        product = self.vendor_product
        if not product:
            return "device_not_found"
        return product

    def get_status(self, **params):
        """Is the device connected or not?"""
        return {
            "status": "connected" if self.active else "disconnected",
            "messages": [],
        }

    @abstractmethod
    def acquire_data(self, connection):
        """Acquire data over the connection."""

    @abstractmethod
    def establish_connection(self):
        """Establish a connection. The connection must be a context manager."""

    def run(self):
        with ExitStack() as exit_stack:
            while True:
                with self._data_lock:
                    self._data = {}
                while not self.active:
                    try:
                        connection = exit_stack.enter_context(
                            self.establish_connection()
                        )
                        self.active = True
                    except Exception:
                        _logger.error("failed to connect to scale")
                        time.sleep(1)
                poll_time = 0
                while self.active:
                    try:
                        # Sleep until approximately exactly self.poll_interval
                        # time has passed since previous iteration.
                        current_time = time.perf_counter()
                        sleep_time = self.poll_interval - (current_time - poll_time)
                        if sleep_time > 0:
                            time.sleep(sleep_time)
                        poll_time = time.perf_counter()

                        data = self.acquire_data(connection)
                        with self._data_lock:
                            self._data = data
                    except ScaleConnectionError:
                        _logger.error("connection with scale lost")
                        exit_stack.close()
                        self.active = False
                    except Exception:
                        # While connection is still active, continue and try
                        # again.
                        _logger.exception("error during acquiring of data")


@app.before_first_request
def before_first_request():
    protocol = config.get("scale_driver", "protocol_name", fallback=None)
    if not protocol:
        raise ValueError("scale_driver.protocol_name is not defined")
    module = import_module(".scale_protocols." + protocol, __package__)
    for _, value in module.__dict__.items():
        try:
            result = issubclass(value, AbstractScaleDriver)
        except Exception:
            continue
        if result and value != AbstractScaleDriver:
            driver = value(config=config)
            driver.start()
            drivers["scale"] = driver
            break
    else:
        raise ValueError(
            "could not find scale protocol class in {}".format(module.__name__)
        )


@app.route("/hw_proxy/scale_read", methods=["POST"])
def scale_read_post():
    return jsonify(
        jsonrpc="2.0",
        result={
            "weight": drivers["scale"].weight,
            # although the unit is sent here as part of the protocol, the odoo
            # pos interface currently ignores it and always assumes kg.
            "unit": "kg",
            "info": drivers["scale"].scale_status,
        },
    )
