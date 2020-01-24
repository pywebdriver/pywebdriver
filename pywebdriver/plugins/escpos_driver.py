# -*- coding: utf-8 -*-
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

from pif import get_public_ip
from pywebdriver import app, config, drivers
from netifaces import interfaces, ifaddresses, AF_INET
from flask import request, jsonify, render_template
from .base_driver import ThreadDriver
from xmlescpos import Layout
from escpos import capabilities
from escpos.magicencode import MagicEncode
import usb.core
import math


meta = {
    'name': "ESCPOS Printer",
    'description': """This plugin add the support of ESCPOS Printer for your
        pywebdriver""",
    'require_pip': ['pyxmlescpos'],
    'require_debian': [],
}

if (
        config.has_option('escpos_driver', 'device_type') and
        config.get('escpos_driver', 'device_type') == 'serial'):
    device_type = 'serial'
else:
    device_type = 'usb'

SUPPORTED_DEVICES = [
    { 'vendor' : 0x04b8, 'product' : 0x0e03, 'name' : 'Epson TM-T20' },
    { 'vendor' : 0x04b8, 'product' : 0x0202, 'name' : 'Epson TM-T70' },
    { 'vendor' : 0x04b8, 'product' : 0x0e15, 'name' : 'Epson TM-T20II' },
]

try:
    if device_type == 'serial':
        from escpos.printer import Serial as POSDriver
    else:
        from escpos.printer import Usb as POSDriver
except ImportError:
    installed = False
    print('ESCPOS: xmlescpos python library not installed')
else:
    class ESCPOSDriver(ThreadDriver, POSDriver):
        """ ESCPOS Printer Driver class for pywebdriver """

        def __init__(self, *args, **kwargs):
            self.eprint = None
            self.vendor_product = None
            ThreadDriver.__init__(self, args, kwargs)

        def connected_usb_devices(self):
            connected = []

            for device in SUPPORTED_DEVICES:
                if usb.core.find(
                        idVendor=device['vendor'],
                        idProduct=device['product']) is not None:
                    connected.append(device)
            return connected

        def open_printer(self):
            if self.device:
                return
            try:
                if device_type == 'usb':
                    printers = self.connected_usb_devices()
                    if printers:
                        printer = printers[0]
                        self.interface = printer.get('interface', 0)
                        self.in_ep = printer.get('in_ep', 0x82)
                        self.out_ep = printer.get('out_ep', 0x01)
                        self.timeout = 0
                        self.profile = capabilities.get_profile(None)
                        self.magic = MagicEncode(self, {})
                        self.open({"idVendor": printer.get('vendor'), "idProduct": printer.get('product')})
                        self.vendor_product = '%s_%s' % (
                            self.idVendor, self.idProduct
                        )
                elif device_type == 'serial':
                    self.devfile = config.get('escpos_driver', 'serial_device_name')
                    self.baudrate = config.getint('escpos_driver', 'serial_baudrate')
                    self.bytesize = config.getint('escpos_driver', 'serial_bytesize')
                    self.timeout = config.getint('escpos_driver', 'serial_timeout')
                    self.open()

            except Exception as e:
                self.set_status('error', str(e))

        def open_cashbox(self, printer):
            self.open_printer()
            self.cashdraw(2)
            self.cashdraw(5)

        def get_status(self, **params):
            messages = []
            self.open_printer()
            if not self.device:
                status = 'disconnected'
            elif device_type == 'serial':
                # Maybe we could do something here to start serial
                status = 'connected'
            else:
                try:
                    if self.is_online():
                        status = 'connected'
                        print("CONNECTED")
                    else:
                        status = 'connecting'
                    # if res['printer']['status_error']:
                    #     status = 'error'
                    #     messages.append(
                    #         'Error code: %i' % res['printer']['status_error'])
                except Exception as err:
                    status = 'error'
                    self.device = False
                    messages.append('Error: %s' % err)

            return {
                'status': status,
                'messages': messages,
            }

        def receipt(self, content):
            Layout(content).format(self)
            self.cut()

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
                    """that network addresses are available""")
                Layout('<div>'+msg+'</div>').format(self)
                self.cut()
            else:
                addr_lines = []
                for ifaceName in interfaces():
                    addresses = [
                        i['addr'] for i in ifaddresses(ifaceName).setdefault(
                            AF_INET, [{'addr': 'No IP addr'}])]
                    addr_lines.append(
                        '<p>'+','.join(addresses) + ' (' + ifaceName + ')' +
                        '</p>')
                msg = _("""
                       <div align="center">
                            <h4>PyWebDriver Software Status</h4>
                            <br/><br/>
                            <h5>IP Addresses:</h5>
                            %s<br/>
                            %s<br/>
                            Port: %i
                       </div>
                """) % (
                    ip + ' (' + _(u'Public') + ')',
                    ''.join(addr_lines),
                    config.getint('flask', 'port'),
                )
                Layout('<div>'+msg+'</div>').format(self)

        # #####################################################################
        # <Odoo Version 7>
        def print_receipt_7(self, receipt):

            def check(string):
                return string is not True and bool(string) and string.strip()

            def price(amount):
                return (
                    "{0:." +
                    str(receipt['precision']['price']) + "f}").format(amount)

            def money(amount):
                return (
                    "{0:." +
                    str(receipt['precision']['money']) + "f}").format(amount)

            def quantity(amount):
                if math.floor(amount) != amount:
                    return (
                        "{0:." +
                        str(receipt['precision']['quantity']) +
                        "f}").format(amount)
                else:
                    return str(amount)

            def printline(left, right='', width=40, ratio=0.5, indent=0):
                lwidth = int(width * ratio)
                rwidth = width - lwidth
                lwidth = lwidth - indent

                left = left[:lwidth]
                if len(left) != lwidth:
                    left = left + ' ' * (lwidth - len(left))

                right = right[-rwidth:]
                if len(right) != rwidth:
                    right = ' ' * (rwidth - len(right)) + right

                return ' ' * indent + left + right + '\n'

            def print_taxes():
                taxes = receipt.get('tax_details', [])
                for tax in taxes:
                    eprint.text(printline(
                        tax['tax']['name'], price(tax['amount']), width=40,
                        ratio=0.6))

            if not self.eprint:
                printers = self.connected_usb_devices()
                if len(printers) > 0:
                    self.eprint = POSDriver(
                        printers[0]['vendor'], printers[0]['product'])
                else:
                    return

            eprint = self.eprint

            # Receipt Header
            if receipt['company'].get('logo', False):
                eprint.set(align='center')
                eprint.print_base64_image(receipt['company']['logo'])
                eprint.text('\n')
            else:
                eprint.set(align='center', type='b', height=2, width=2)
                eprint.text(receipt['company']['name'] + '\n')

            eprint.set(align='center', type='b')
            if check(receipt['company'].get('contact_address', False)):
                eprint.text(receipt['company']['contact_address'] + '\n')
            if check(receipt['company'].get('phone', False)):
                eprint.text(_(u'Tel: ') + receipt['company']['phone'] + '\n')
            if check(receipt['company'].get('vat', False)):
                eprint.text(_(u'VAT: ') + receipt['company']['vat'] + '\n')
            if check(receipt['company'].get('email', False)):
                eprint.text(receipt['company']['email'] + '\n')
            if check(receipt['company'].get('website', False)):
                eprint.text(receipt['company']['website'] + '\n')
            if check(receipt.get('header')):
                eprint.text(receipt['header'] + '\n')
            if check(receipt.get('cashier')):
                eprint.text('-' * 32 + '\n')
                eprint.text(_(u'Served by ') + receipt['cashier'] + '\n')

            # Orderlines
            if config.getboolean('odoo', 'orderline_price_with_tax'):
                orderline_price_field = 'price_with_tax'
            else:
                orderline_price_field = 'price_without_tax'
            eprint.text('\n\n')
            eprint.set(align='center')
            for line in receipt['orderlines']:
                pricestr = price(line[orderline_price_field])
                if line['discount'] == 0\
                        and line['unit_name'] == 'Unit(s)'\
                        and line['quantity'] == 1:
                    eprint.text(printline(
                        line['product_name'], pricestr, ratio=0.6))
                else:
                    eprint.text(printline(line['product_name'], ratio=0.6))
                    if line['discount'] != 0:
                        eprint.text(printline(
                            _(u'Discount: ') + str(line['discount'])+'%',
                            ratio=0.6, indent=2))
                    if line['unit_name'] == 'Unit(s)':
                        eprint.text(printline(
                            quantity(line['quantity']) + ' x ' +
                            price(line['price']), pricestr, ratio=0.6,
                            indent=2))
                    else:
                        eprint.text(printline(
                            quantity(line['quantity']) + ' ' +
                            line['unit_name'] + ' x ' + price(line['price']),
                            pricestr, ratio=0.6, indent=2))

            # Subtotal if the taxes are not included
            taxincluded = True
            if money(receipt['subtotal']) != money(receipt['total_with_tax']):
                eprint.text(printline('', '-------'))
                eprint.text(printline(
                    _(u'Subtotal'), money(receipt['subtotal']), width=40,
                    ratio=0.6))
                print_taxes()
                eprint.text(printline(
                    _(u'Taxes'), money(receipt['total_tax']), width=40,
                    ratio=0.6))
                taxincluded = False

            # Total
            eprint.text(printline('', '-------'))
            eprint.set(align='center', height=2)
            eprint.text(printline(
                _(u'         TOTAL'), money(receipt['total_with_tax']),
                width=40, ratio=0.6))
            eprint.text('\n\n')

            # Paymentlines
            eprint.set(align='center')
            for line in receipt['paymentlines']:
                eprint.text(printline(
                    line['journal'], money(line['amount']), ratio=0.6))

            eprint.text('\n')
            eprint.set(align='center', height=2)
            eprint.text(printline(
                _(u'        CHANGE'), money(receipt['change']), width=40,
                ratio=0.6))
            eprint.set(align='center')
            eprint.text('\n')

            # Extra Payment info
            if receipt['total_discount'] != 0:
                eprint.text(printline(
                    _(u'Discounts'), money(receipt['total_discount']),
                    width=40, ratio=0.6))
            if taxincluded:
                print_taxes()
                eprint.text(printline(
                    _(u'Taxes'), money(receipt['total_tax']), width=40,
                    ratio=0.6))

            # Footer
            if check(receipt.get('footer')):
                eprint.text('\n'+receipt['footer']+'\n\n')
            eprint.text(receipt['name']+'\n')
            eprint.text(
                str(receipt['date']['date']).zfill(2) +
                '/' + str(receipt['date']['month']+1).zfill(2) +
                '/' + str(receipt['date']['year']).zfill(4) +
                ' ' + str(receipt['date']['hour']).zfill(2) +
                ':' + str(receipt['date']['minute']).zfill(2))

            eprint.cut()

        # </Odoo Version 7>
        # #####################################################################

    driver = ESCPOSDriver(app.config)
    drivers['escpos'] = driver
    installed = True

    @app.route(
            '/hw_proxy/print_xml_receipt',
            methods=['POST', 'GET', 'PUT'])
    def print_xml_receipt_json():
        """ For Odoo 8.0+"""

        driver.open_printer()
        receipt = request.json['params']['receipt']
        driver.push_task('receipt', receipt)

        return jsonify(jsonrpc='2.0', result=True)

    @app.route('/print_status.html', methods=['GET'])
    def print_status_http():
        driver.push_task('printstatus')
        return render_template('print_status.html')

    @app.route(
        '/hw_proxy/open_cashbox',
        methods=['POST', 'GET', 'PUT'])
    def open_cashbox():
        driver.push_task('open_cashbox')
        return jsonify(jsonrpc='2.0', result=True)
