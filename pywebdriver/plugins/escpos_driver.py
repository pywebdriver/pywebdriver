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
meta = {
    'name': "ESCPOS Printer",
    'description': """This plugin add the support of ESCPOS Printer for your
        pywebdriver""",
    'require_pip': ['pyxmlescpos'],
    'require_debian': [],
}

from pywebdriver import app, config, drivers
from flask_cors import cross_origin
from flask import request, jsonify
from base_driver import ThreadDriver, check
import simplejson
import usb.core

try:
    from xmlescpos.printer import Usb
    from xmlescpos.supported_devices import device_list
except:
    installed=False
else:
    installed=True
    class ESCPOSDriver(ThreadDriver, Usb):
        """ ESCPOS Printer Driver class for pywebdriver """

        def __init__(self, *args, **kwargs):
            self.vendor_product = None
            ThreadDriver.__init__(self, args, kwargs)

        def supported_devices(self):
            return device_list

        def connected_usb_devices(self):
            connected = []
            
            for device in self.supported_devices():
                if usb.core.find(idVendor=device['vendor'], idProduct=device['product']) != None:
                    connected.append(device)

            return connected

        def open_printer(self):
            
            if self.device:
                return

            try:
                printers = self.connected_usb_devices()
                if printers:
                    printer = printers[0]
                    self.idVendor = printer.get('vendor')
                    self.idProduct = printer.get('product')
                    self.interface = printer.get('interface', 0)
                    self.in_ep = printer.get('in_ep', 0x82)
                    self.out_ep = printer.get('out_ep', 0x01)
                    self.open()
            
            except Exception as e:
                self.set_status('error',str(e))

        def open_cashbox(self,printer):
            self.open_printer()
            self.cashdraw(2)
            self.cashdraw(5)

        def get_status(self):
            self.open_printer()
            if not self.device:
                res = []
                status = 'disconnected'
            else:
                res = self.get_printer_status()
                import pprint
                pprint.pprint(res)

                if res['printer']['online']:
                    status = 'connected'
                else:
                    status = 'connecting'
            res['state'] = {'status': status}
            return res

        def print_status(self,eprint):
            #<PyWebDriver> Full refactoring of the function to allow
            # localisation and to make more easy the search of the ip
            ip = get_public_ip()
            eprint.text('\n\n')
            eprint.set(align='center',type='b',height=2,width=2)
            eprint.text(_(u'PyWebDriver Software Status'))
            eprint.text('\n\n')
            eprint.set(align='center')

            if not ip:
                msg = _(
                    """ERROR: Could not connect to LAN\n\n"""
                    """Please check that your system is correc-\n"""
                    """tly connected with a network cable,\n"""
                    """ that the LAN is setup with DHCP, and\n"""
                    """that network addresses are available""")
                eprint.text(msg)
            else:
                eprint.text(_(u'IP Addresses:') + '\n')
                eprint.text(ip + ' (' + _(u'Public') + ')\n')
                for ifaceName in interfaces():
                    pass
                    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
                    eprint.text(', '.join(addresses) + ' (' + ifaceName + ')\n')
                eprint.text('\n' + _(u'Port:') + '\n')
                eprint.text(self.port + '\n')

            eprint.text('\n\n')
            eprint.cut()

drivers['escpos'] = ESCPOSDriver(app.config)

@app.route(
        '/hw_proxy/print_xml_receipt',
        methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def print_xml_receipt_json():
    """ For Odoo 8.0+"""
    
    driver = drivers['escpos']
    driver.open_printer()
    receipt = request.json['params']['receipt']
    driver.push_task('receipt', receipt)
    
    return jsonify(jsonrpc='2.0', result=True)
