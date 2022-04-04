###############################################################################
#
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#   @author Sylvain CALADOR <sylvain.calador@akretion.com>
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

import fnmatch
import logging
import math
from configparser import NoOptionError

import usb.core
from flask import jsonify, render_template, request
from netifaces import AF_INET, ifaddresses, interfaces
from pif import get_public_ip
from xmlescpos import Layout

from pywebdriver import app, config, drivers

from .base_driver import ThreadDriver

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
elif (
    config.has_option("escpos_driver", "device_type")
    and config.get("escpos_driver", "device_type") == "network"
):
    device_type = "network"
elif (
    config.has_option("escpos_driver", "device_type")
    and config.get("escpos_driver", "device_type") == "dummy"
):
    device_type = "dummy"
else:
    device_type = "usb"

SUPPORTED_DEVICES = [
    # Don't add 2 entries with the same vendor and product IDs
    # Epson TM-T70, TM-T70II and Epson TM-P20 have the same vendor/product IDs
    {"vendor": 0x04B8, "product": 0x0E03, "name": "Epson TM-T20"},
    {"vendor": 0x04B8, "product": 0x0202, "name": "Epson TM-T70"},
    {"vendor": 0x04B8, "product": 0x0E15, "name": "Epson TM-T20II"},
    {"vendor": 0x04B8, "product": 0x0E28, "name": "Epson TM-T20III"},
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
    elif device_type == "dummy":
        from escpos.printer import Dummy as POSDriver
    elif device_type == "network":
        from escpos.printer import Network as POSDriver
    else:
        from escpos.printer import Usb as POSDriver
except ImportError:
    installed = False
    print("ESCPOS: xmlescpos python library not installed")
else:

    class ESCPOSDriver(ThreadDriver, POSDriver):
        """ ESCPOS Printer Driver class for pywebdriver """

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
            elif device_type == "dummy":
                POSDriver.__init__(self, **kwargs)
            elif device_type == "network":
                super(POSDriver, self).__init__(**kwargs)
                self.host = None
                self.port = 9100
                self.timeout = 60
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

        def open(self):
            """Open TCP socket with ``socket``-library and set it as escpos device"""
            if device_type == "network" and not self.host:
                print("Could not open socket for {}".format(self.host))
            else:
                super(ESCPOSDriver, self).open()

        def get_vendor_product(self):
            return "escpos-icon"

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

        def open_printer(self, printer_ip=None):
            if printer_ip:
                self.host = printer_ip
                self.open()
                return

            if self.device:
                return
            try:
                self.open(*self.open_args)
                if device_type == "win32":
                    self.device = self.hPrinter
            except Exception as e:
                self.set_status("error", e)

        def open_cashbox(self, printer):
            self.open_printer()
            self.cashdraw(2)
            self.cashdraw(5)
            self.close()

        def get_status(self, **params):
            messages = []
            self.open_printer()
            if not self.device:
                status = "disconnected"
            elif device_type == "serial":
                # Maybe we could do something here to start serial
                status = "connected"
            elif device_type == "usb":
                try:
                    if self.is_online():
                        status = "connected"
                    else:
                        status = "connecting"
                    # if res['printer']['status_error']:
                    #     status = 'error'
                    #     messages.append(
                    #         'Error code: %i' % res['printer']['status_error'])
                except Exception as err:
                    status = "error"
                    self.device = False
                    messages.append("Error: %s" % err)
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
            self.close()
            return {
                "status": status,
                "messages": messages,
            }

        def receipt_jpeg(self, b64image):
            content = '<img src="data:image/png;base64, {}" />'.format(b64image)
            self.receipt(content)

        def receipt(self, content):
            receipt = content.get("receipt")
            printer_ip = content.get("printer_ip")
            self.open_printer(printer_ip)
            Layout(receipt).format(self)
            self.cut()
            self.close()

        def printstatus(self, eprint):
            # <PyWebDriver> Full refactoring of the function to allow
            # localisation and to make more easy the search of the ip

            self.open_printer()
            ip = get_public_ip()

            if not ip:
                msg = _(
                    """ERROR: Could not connect to LAN<br/><br/>"""
                    """Please check that your system is correc-<br/>"""
                    """tly connected with a network cable,<br/>"""
                    """ that the LAN is setup with DHCP, and<br/>"""
                    """that network addresses are available"""
                )
                Layout("<div>" + msg + "</div>").format(self)
                self.cut()
            else:
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
                msg = _(
                    """
                       <div align="center">
                            <h4>PyWebDriver Software Status</h4>
                            <br/><br/>
                            <h5>IP Addresses:</h5>
                            %s<br/>
                            %s<br/>
                            Port: %i
                       </div>
                """
                ) % (
                    ip + " (" + _(u"Public") + ")",
                    "".join(addr_lines),
                    config.getint("flask", "port"),
                )
                Layout("<div>" + msg + "</div>").format(self)
                self.close()

        # #####################################################################
        # <Odoo Version 7>
        def print_receipt_7(self, receipt):
            def check(string):
                return string is not True and bool(string) and string.strip()

            def price(amount):
                return ("{0:." + str(receipt["precision"]["price"]) + "f}").format(
                    amount
                )

            def money(amount):
                return ("{0:." + str(receipt["precision"]["money"]) + "f}").format(
                    amount
                )

            def quantity(amount):
                if math.floor(amount) != amount:
                    return (
                        "{0:." + str(receipt["precision"]["quantity"]) + "f}"
                    ).format(amount)
                else:
                    return str(amount)

            def printline(left, right="", width=40, ratio=0.5, indent=0):
                lwidth = int(width * ratio)
                rwidth = width - lwidth
                lwidth = lwidth - indent

                left = left[:lwidth]
                if len(left) != lwidth:
                    left = left + " " * (lwidth - len(left))

                right = right[-rwidth:]
                if len(right) != rwidth:
                    right = " " * (rwidth - len(right)) + right

                return " " * indent + left + right + "\n"

            def print_taxes():
                taxes = receipt.get("tax_details", [])
                for tax in taxes:
                    eprint.text(
                        printline(
                            tax["tax"]["name"],
                            price(tax["amount"]),
                            width=40,
                            ratio=0.6,
                        )
                    )

            if not self.eprint:
                printers = self.connected_usb_devices()
                if len(printers) > 0:
                    self.eprint = POSDriver(
                        printers[0]["vendor"], printers[0]["product"]
                    )
                else:
                    return

            eprint = self.eprint

            # Receipt Header
            if receipt["company"].get("logo", False):
                eprint.set(align="center")
                eprint.print_base64_image(receipt["company"]["logo"])
                eprint.text("\n")
            else:
                eprint.set(align="center", type="b", height=2, width=2)
                eprint.text(receipt["company"]["name"] + "\n")

            eprint.set(align="center", type="b")
            if check(receipt["company"].get("contact_address", False)):
                eprint.text(receipt["company"]["contact_address"] + "\n")
            if check(receipt["company"].get("phone", False)):
                eprint.text(_(u"Tel: ") + receipt["company"]["phone"] + "\n")
            if check(receipt["company"].get("vat", False)):
                eprint.text(_(u"VAT: ") + receipt["company"]["vat"] + "\n")
            if check(receipt["company"].get("email", False)):
                eprint.text(receipt["company"]["email"] + "\n")
            if check(receipt["company"].get("website", False)):
                eprint.text(receipt["company"]["website"] + "\n")
            if check(receipt.get("header")):
                eprint.text(receipt["header"] + "\n")
            if check(receipt.get("cashier")):
                eprint.text("-" * 32 + "\n")
                eprint.text(_(u"Served by ") + receipt["cashier"] + "\n")

            # Orderlines
            if config.getboolean("odoo", "orderline_price_with_tax"):
                orderline_price_field = "price_with_tax"
            else:
                orderline_price_field = "price_without_tax"
            eprint.text("\n\n")
            eprint.set(align="center")
            for line in receipt["orderlines"]:
                pricestr = price(line[orderline_price_field])
                if (
                    line["discount"] == 0
                    and line["unit_name"] == "Unit(s)"
                    and line["quantity"] == 1
                ):
                    eprint.text(printline(line["product_name"], pricestr, ratio=0.6))
                else:
                    eprint.text(printline(line["product_name"], ratio=0.6))
                    if line["discount"] != 0:
                        eprint.text(
                            printline(
                                _(u"Discount: ") + str(line["discount"]) + "%",
                                ratio=0.6,
                                indent=2,
                            )
                        )
                    if line["unit_name"] == "Unit(s)":
                        eprint.text(
                            printline(
                                quantity(line["quantity"])
                                + " x "
                                + price(line["price"]),
                                pricestr,
                                ratio=0.6,
                                indent=2,
                            )
                        )
                    else:
                        eprint.text(
                            printline(
                                quantity(line["quantity"])
                                + " "
                                + line["unit_name"]
                                + " x "
                                + price(line["price"]),
                                pricestr,
                                ratio=0.6,
                                indent=2,
                            )
                        )

            # Subtotal if the taxes are not included
            taxincluded = True
            if money(receipt["subtotal"]) != money(receipt["total_with_tax"]):
                eprint.text(printline("", "-------"))
                eprint.text(
                    printline(
                        _(u"Subtotal"), money(receipt["subtotal"]), width=40, ratio=0.6
                    )
                )
                print_taxes()
                eprint.text(
                    printline(
                        _(u"Taxes"), money(receipt["total_tax"]), width=40, ratio=0.6
                    )
                )
                taxincluded = False

            # Total
            eprint.text(printline("", "-------"))
            eprint.set(align="center", height=2)
            eprint.text(
                printline(
                    _(u"         TOTAL"),
                    money(receipt["total_with_tax"]),
                    width=40,
                    ratio=0.6,
                )
            )
            eprint.text("\n\n")

            # Paymentlines
            eprint.set(align="center")
            for line in receipt["paymentlines"]:
                eprint.text(
                    printline(line["journal"], money(line["amount"]), ratio=0.6)
                )

            eprint.text("\n")
            eprint.set(align="center", height=2)
            eprint.text(
                printline(
                    _(u"        CHANGE"), money(receipt["change"]), width=40, ratio=0.6
                )
            )
            eprint.set(align="center")
            eprint.text("\n")

            # Extra Payment info
            if receipt["total_discount"] != 0:
                eprint.text(
                    printline(
                        _(u"Discounts"),
                        money(receipt["total_discount"]),
                        width=40,
                        ratio=0.6,
                    )
                )
            if taxincluded:
                print_taxes()
                eprint.text(
                    printline(
                        _(u"Taxes"), money(receipt["total_tax"]), width=40, ratio=0.6
                    )
                )

            # Footer
            if check(receipt.get("footer")):
                eprint.text("\n" + receipt["footer"] + "\n\n")
            eprint.text(receipt["name"] + "\n")
            eprint.text(
                str(receipt["date"]["date"]).zfill(2)
                + "/"
                + str(receipt["date"]["month"] + 1).zfill(2)
                + "/"
                + str(receipt["date"]["year"]).zfill(4)
                + " "
                + str(receipt["date"]["hour"]).zfill(2)
                + ":"
                + str(receipt["date"]["minute"]).zfill(2)
            )

            eprint.cut()

        # </Odoo Version 7>
        # #####################################################################

    driver = ESCPOSDriver(app.config)
    drivers["escpos"] = driver
    installed = True

    @app.route("/hw_proxy/default_printer_action", methods=["POST", "GET", "PUT"])
    def default_printer_action():
        """ For Odoo 13.0+"""

        action = request.json["params"]["data"]["action"]
        if action == "print_receipt":
            receipt = request.json["params"]["data"]["receipt"]
            driver.push_task("receipt_jpeg", receipt)
        if action == "cashbox":
            driver.push_task("open_cashbox")
        return jsonify(jsonrpc="2.0", result=True)

    @app.route("/hw_proxy/print_xml_receipt", methods=["POST", "GET", "PUT"])
    def print_xml_receipt_json():
        """ For Odoo 8.0+"""

        content = dict(
            receipt=request.json["params"]["receipt"].replace("ean13", "EAN13"),
            printer_ip=request.json["params"].get("proxy"),
        )
        driver.push_task("receipt", content)

        return jsonify(jsonrpc="2.0", result=True)

    @app.route("/print_status.html", methods=["GET"])
    def print_status_http():
        driver.push_task("printstatus")
        return render_template("print_status.html")

    @app.route("/hw_proxy/open_cashbox", methods=["POST", "GET", "PUT"])
    def open_cashbox():
        driver.push_task("open_cashbox")
        return jsonify(jsonrpc="2.0", result=True)
