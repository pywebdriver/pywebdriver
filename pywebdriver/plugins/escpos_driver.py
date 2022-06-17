# Copyright (C) 2014-Today Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Sylvain CALADOR <sylvain.calador@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import fnmatch
import logging
from configparser import NoOptionError

import usb.core
import errno
from flask import jsonify, render_template, request
from netifaces import AF_INET, ifaddresses, interfaces
from xmlescpos import Layout

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver

ENODEV = errno.__dict__.get('ENODEV', None),

meta = {
    "name": "ESCPOS Printer",
    "description": """This plugin add the support of ESCPOS Printer for your
        pywebdriver""",
    "require_pip": ["pyxmlescpos"],
    "require_debian": [],
}

if (
    config.has_option("escpos_driver", "device_type")
    and config.get("escpos_driver", "device_type") == "serial"
):
    device_type = "serial"
elif (
    config.has_option("escpos_driver", "device_type")
    and config.get("escpos_driver", "device_type") == "win32"
):
    device_type = "win32"
else:
    device_type = "usb"

SUPPORTED_DEVICES = [
    # Don't add 2 entries with the same vendor and product IDs
    # Epson TM-T70, TM-T70II and Epson TM-P20 have the same vendor/product IDs
    {"vendor": 0x04B8, "product": 0x0E03, "name": "Epson TM-T20"},
    {"vendor": 0x04B8, "product": 0x0202, "name": "Epson TM-T70"},
    {"vendor": 0x04B8, "product": 0x0E15, "name": "Epson TM-T20II"},
    {"vendor": 0x04B8, "product": 0x0E28, "name": "Epson TM-T20III"},
    {"vendor": 0x0525, "product": 0xA700, "name": "Netchip POS Printer Aures ODP 333"},
]

_logger = logging.getLogger(__name__)

try:  # noqa C901
    if device_type == "serial":
        from escpos.printer import Serial as POSDriver
    elif device_type == "win32":
        import win32print
        from escpos.printer import Win32Raw as POSDriver

        PRINTER_STATUS_DICT = {
            0: {"title": "AVAILABLE", "usable": True},
            win32print.PRINTER_STATUS_PAUSED: {"title": "PAUSED", "usable": False},
            win32print.PRINTER_STATUS_ERROR: {"title": "ERROR", "usable": False},
            win32print.PRINTER_STATUS_PENDING_DELETION: {
                "title": "PENDING_DELETION",
                "usable": False,
            },
            win32print.PRINTER_STATUS_PAPER_JAM: {
                "title": "PAPER_JAM",
                "usable": False,
            },
            win32print.PRINTER_STATUS_PAPER_OUT: {
                "title": "PAPER_OUT",
                "usable": False,
            },
            win32print.PRINTER_STATUS_MANUAL_FEED: {
                "title": "MANUAL_FEED",
                "usable": False,
            },
            win32print.PRINTER_STATUS_PAPER_PROBLEM: {
                "title": "PAPER_PROBLEM",
                "usable": False,
            },
            win32print.PRINTER_STATUS_OFFLINE: {"title": "OFFLINE", "usable": False},
            win32print.PRINTER_STATUS_IO_ACTIVE: {
                "title": "IO_ACTIVE",
                "usable": False,
            },
            win32print.PRINTER_STATUS_BUSY: {"title": "BUSY", "usable": False},
            win32print.PRINTER_STATUS_PRINTING: {"title": "PRINTING", "usable": True},
            win32print.PRINTER_STATUS_OUTPUT_BIN_FULL: {
                "title": "OUTPUT_BIN_FULL",
                "usable": False,
            },
            win32print.PRINTER_STATUS_NOT_AVAILABLE: {
                "title": "NOT_AVAILABLE",
                "usable": False,
            },
            win32print.PRINTER_STATUS_WAITING: {"title": "WAITING", "usable": True},
            win32print.PRINTER_STATUS_PROCESSING: {
                "title": "PROCESSING",
                "usable": True,
            },
            win32print.PRINTER_STATUS_INITIALIZING: {
                "title": "INITIALIZING",
                "usable": True,
            },
            win32print.PRINTER_STATUS_WARMING_UP: {
                "title": "WARMING_UP",
                "usable": True,
            },
            win32print.PRINTER_STATUS_TONER_LOW: {"title": "TONER_LOW", "usable": True},
            win32print.PRINTER_STATUS_NO_TONER: {"title": "NO_TONER", "usable": False},
            win32print.PRINTER_STATUS_PAGE_PUNT: {
                "title": "PAGE_PUNT",
                "usable": False,
            },
            win32print.PRINTER_STATUS_USER_INTERVENTION: {
                "title": "USER_INTERVENTION",
                "usable": False,
            },
            win32print.PRINTER_STATUS_OUT_OF_MEMORY: {
                "title": "OUT_OF_MEMORY",
                "usable": False,
            },
            win32print.PRINTER_STATUS_DOOR_OPEN: {"title": "DOOR_OPEN", "usable": True},
            win32print.PRINTER_STATUS_SERVER_UNKNOWN: {
                "title": "SERVER_UNKNOWN",
                "usable": False,
            },
            win32print.PRINTER_STATUS_POWER_SAVE: {
                "title": "POWER_SAVE",
                "usable": True,
            },
        }
    else:
        from escpos.printer import Usb as POSDriver
except ImportError:
    installed = False
    print("ESCPOS: xmlescpos python library not installed")
else:

    class ESCPOSDriver(ThreadDriver, POSDriver):
        """ESCPOS Printer Driver class for pywebdriver"""

        def __init__(self, *args, **kwargs):
            self.eprint = None
            self.vendor_product = None
            self.open_args = []
            if device_type == "usb":
                printers = self.connected_usb_devices()
                if printers:
                    printer = printers[0]
                    idVendor = printer.get("vendor")
                    idProduct = printer.get("product")
                    usb_args = {"idVendor": idVendor, "idProduct": idProduct}
                    kwargs["in_ep"] = printer.get("in_ep", 0x82)
                    kwargs["out_ep"] = printer.get("out_ep", 0x01)
                    kwargs["timeout"] = 0
                    POSDriver.__init__(self, idVendor, idProduct, **kwargs)
                    self.open_args.append(usb_args)  # First open_arg is usb_args
            elif device_type == "serial":
                kwargs["devfile"] = config.get("escpos_driver", "serial_device_name")
                kwargs["baudrate"] = config.getint("escpos_driver", "serial_baudrate")
                kwargs["bytesize"] = config.getint("escpos_driver", "serial_bytesize")
                kwargs["timeout"] = config.getint("escpos_driver", "serial_timeout")
                POSDriver.__init__(self, **kwargs)
            elif device_type == "win32":
                try:
                    kwargs["printer_name"] = config.get("escpos_driver", "printer_name")
                except NoOptionError:
                    config_printer_names = config.get(
                        "escpos_driver", "printer_names"
                    ).split(",")
                    printers_list = win32print.EnumPrinters(
                        win32print.PRINTER_ENUM_NAME, None, 2
                    )
                    printers_dict = {
                        item["pPrinterName"]: item for item in printers_list
                    }
                    i = 0
                    while i < len(config_printer_names):
                        config_printer_name = config_printer_names[i]
                        i += 1
                        for printer_name, printer in printers_dict.items():
                            if fnmatch.fnmatch(printer_name, config_printer_name):
                                status = PRINTER_STATUS_DICT.get(printer["Status"])
                                _logger.debug([printer_name, status])
                                if status and "usable" in status and status["usable"]:
                                    kwargs[
                                        "printer_name"
                                    ] = printer_name  # Printer will be used
                                    break
                        if "printer_name" in kwargs:
                            break
                finally:
                    if "printer_name" not in kwargs:
                        kwargs["printer_name"] = "escpos"  # To avoid crashing
                    POSDriver.__init__(self, **kwargs)
            ThreadDriver.__init__(self, *args, **kwargs)

        def get_vendor_product(self):
            return "escpos-icon"

        def printer_available(self):
            if device_type == "usb":
                return (
                    usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
                    is not None
                )
            # TODO: Determine the state of the printer for different device_type
            return False

        def connected_usb_devices(self):
            connected = []

            for device in SUPPORTED_DEVICES:
                if (
                    usb.core.find(
                        idVendor=device["vendor"], idProduct=device["product"]
                    )
                    is not None
                ):
                    connected.append(device)
            return connected

        def open_printer(self):
            # Check if the printer is still available and wasn't disconnected
            if not self.printer_available():
                self.close()
                return

            if self.device:
                if device_type == "usb":
                    # Device was previously initialized
                    # Try writing to it to see if it is still available
                    # If we get Error ENODEV it might have been temporarily disconnected
                    # -> try to reopen
                    # Otherwise no reopening is neccessary
                    try:
                        self._raw("")
                    except usb.core.USBError as e:
                        if e.errno != ENODEV:
                            self.set_status("error", e)
                        _logger.info("Printer was disconnected. Reconnecting")
                    else:
                        return
                else:
                    return

            try:
                self.open(*self.open_args)
                if device_type == "win32":
                    self.device = self.hPrinter
            except Exception as e:
                self.set_status("error", e)
                self.close()

        def open_cashbox(self, printer):
            self.open_printer()
            if not self.device:
                return

            self.cashdraw(2)
            self.cashdraw(5)

        def get_status(self, **params):
            messages = []
            self.open_printer()
            if not self.device:
                status = "disconnected"
            elif device_type == "serial":
                # Maybe we could do something here to start serial
                status = "connected"
            elif device_type == "usb":
                status = "connected"
            elif device_type == "win32":
                messages.append(self.printer_name)
                result = win32print.GetPrinter(self.device, 2)
                status = PRINTER_STATUS_DICT.get(result["Status"])
                if status:
                    messages.append(status["title"])
                else:
                    messages.append("UNKNOWN: {}".format(result["Status"]))
                if not status or status["title"] in ["OFFLINE", "NOT_AVAILABLE"]:
                    status = "disconnected"
                else:
                    status = "connected"
            else:
                status = "disconnected"
            return {
                "status": status,
                "messages": messages,
            }

        def receipt_jpeg(self, b64image):
            content = '<img src="data:image/png;base64, {}" />'.format(b64image)
            self.receipt(content)

        def receipt(self, content):
            self.open_printer()
            if not self.device:
                return

            Layout(content).format(self)
            self.cut()

        def printstatus(self, eprint):

            self.open_printer()
            if not self.device:
                return

            addr_lines = []
            for ifaceName in interfaces():
                addresses = [
                    i["addr"]
                    for i in ifaddresses(ifaceName).setdefault(
                        AF_INET, [{"addr": "No IP addr"}]
                    )
                ]
                addr_lines.append(
                    "<p>" + ",".join(addresses) + " (" + ifaceName + ")" + "</p>"
                )
            msg = (
                _(
                    """
                   <div align="center">
                        <h4>PyWebDriver Software Status</h4>
                        <br/><br/>
                        <h5>IP Addresses:</h5>
                        %s<br/>
                        Port: %i
                   </div>
            """
                )
                % (
                    "".join(addr_lines),
                    config.getint("flask", "port"),
                )
            )
            self.receipt(msg)

    driver = ESCPOSDriver(app.config)
    drivers["escpos"] = driver
    installed = True

    @app.route("/hw_proxy/default_printer_action", methods=["POST", "GET", "PUT"])
    def default_printer_action():
        """For Odoo 13.0+"""

        action = request.json["params"]["data"]["action"]
        if action == "print_receipt":
            receipt = request.json["params"]["data"]["receipt"]
            driver.push_task("receipt_jpeg", receipt)
        if action == "cashbox":
            driver.push_task("open_cashbox")
        return jsonify(jsonrpc="2.0", result=True)

    @app.route("/hw_proxy/print_xml_receipt", methods=["POST", "GET", "PUT"])
    def print_xml_receipt_json():
        """For Odoo 8.0+"""

        receipt = request.json["params"]["receipt"].replace("ean13", "EAN13")
        driver.push_task("receipt", receipt)

        return jsonify(jsonrpc="2.0", result=True)

    @app.route("/print_status.html", methods=["GET"])
    def print_status_http():
        driver.push_task("printstatus")
        return render_template("print_status.html")

    @app.route("/hw_proxy/open_cashbox", methods=["POST", "GET", "PUT"])
    def open_cashbox():
        driver.push_task("open_cashbox")
        return jsonify(jsonrpc="2.0", result=True)
