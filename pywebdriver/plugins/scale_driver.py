# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Class API for implementing a weighing scale."""

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


class AbstractScaleDriver(Thread, AbstractDriver, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, daemon=True, **kwargs)

        self.active = False
        self.config = config
        self.connection = None
        self.data = {}
        self.data_lock = RLock()
        self.vendor_product = None

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

    @property
    def poll_interval(self):
        """Read the poll interval from the config."""
        return self.config.getfloat("scale_driver", "poll_interval", fallback=0.2)

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

    @abstractmethod
    def is_connection_active(self, connection):
        """Ascertain whether the connection is active and healthy."""

    def run(self):
        with ExitStack() as exit_stack:
            while True:
                while not self.active:
                    try:
                        connection = exit_stack.enter_context(
                            self.establish_connection()
                        )
                        self.active = True
                    except Exception:
                        _logger.error("failed to connect to scale")
                        time.sleep(1)
                while True:
                    try:
                        data = self.acquire_data(connection)
                        with self.data_lock:
                            self.data = data
                        time.sleep(self.poll_interval)
                    except Exception:
                        _logger.exception("error during acquiring of data")
                        if not self.is_connection_active(connection):
                            # Force-close the connection.
                            exit_stack.close()
                            self.active = False
                            break
                        # While connection is still active, try again.
                        continue


@app.before_first_request
def before_first_request():
    global driver
    protocol = config.get("scale_driver", "protocol_name", fallback=None)
    if not protocol:
        raise ValueError("scale_driver.protocol_name is not defined")
    module = import_module("." + protocol, __package__)
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


@app.route("/hw_proxy/weight", methods=["GET"])
def read_weight():
    return jsonify(**{"value": driver.weight, "status": driver.scale_status})


@app.route("/hw_proxy/scale_read", methods=["POST"])
def read_weight_post():
    return jsonify(
        jsonrpc="2.0",
        result={
            "weight": driver.weight,
            "unit": "kg",
            "info": "ok",
        },
    )
