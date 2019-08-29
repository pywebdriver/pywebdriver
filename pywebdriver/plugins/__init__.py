from pywebdriver import config

from configparser import NoOptionError
from importlib import import_module

DEFAULT_DRIVERS = [
    'cups_driver',
    'display_driver',
    'escpos_driver',
    'serial_driver',
    'signature_driver',
    'telium_driver',
    'opcua_driver',
    'odoo7',
    'odoo8',
]

try:
    drivers = config.get('application', 'drivers').split(',')
except NoOptionError:
    drivers = DEFAULT_DRIVERS

for driver in drivers:
    globals()[driver] = import_module('.'+driver, __package__)
