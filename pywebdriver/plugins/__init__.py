import logging
from configparser import NoOptionError
from importlib import import_module

from pywebdriver import config

_logger = logging.getLogger(__name__)

DEFAULT_DRIVERS = [
    "cups_driver",
    "win32print_driver",
    "display_driver",
    "escpos_driver",
    "scale_driver",
    "serial_driver",
    "signature_driver",
    "telium_driver",
    "opcua_driver",
    "odoo8",
]

try:
    drivers = config.get("application", "drivers").split(",")
except NoOptionError:
    drivers = DEFAULT_DRIVERS

for driver in drivers:
    try:
        globals()[driver] = import_module("." + driver, __package__)
    except ImportError as e:
        _logger.warning("Skipping driver %s: %s", driver, e)
