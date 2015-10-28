# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
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

from pywebdriver import app, config, drivers
from flask_cors import cross_origin
from flask import request, jsonify, render_template
from base_driver import ThreadDriver, check
import simplejson
import pypostelium
import simplejson as json
from datetime import datetime

class TeliumDriver(ThreadDriver, pypostelium.Driver):
    """ Telium Driver class for pywebdriver """

    def __init__(self, *args, **kwargs):
        ThreadDriver.__init__(self)
        pypostelium.Driver.__init__(self, *args, **kwargs)
        # TODO : FIXME : Remove once 'status-posdisplay' branch is merged
        self.vendor_product = None

    def get_payment_info_from_price(self, price, payment_mode):
        return {
            'amount': price,
            'payment_mode': payment_mode,
            'currency_iso': 'EUR',
        }

    def get_status(self):
        self.status = {'status': 'connected', 'messages': []}

        # When I use the POS, it regularly goes through that code
        # and sends 999.99 to the credit card reader !!!
        # Si I comment this line -- Alexis
        # telium_driver.push_task('transaction_start', json.dumps(
        #    self.get_payment_info_from_price(999.99, 'card'), sort_keys=True))
        if self.status['status'] == 'connected':
            # TODO Improve : Get the real modele connected
            self.vendor_product = 'telium_image'
        else:
            self.vendor_product = False
        return self.status

driver_config = {}
if config.get('telium_driver', 'device_name'):
    driver_config['telium_terminal_device_name'] =\
        config.get('telium_driver', 'device_name')
if config.getint('telium_driver', 'device_rate'):
    driver_config['telium_terminal_device_rate'] =\
        config.getint('telium_driver', 'device_rate')

telium_driver = TeliumDriver(driver_config)
drivers['telium'] = telium_driver


@app.route(
    '/hw_proxy/payment_terminal_transaction_start',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def payment_terminal_transaction_start():
    app.logger.debug('Telium: Call payment_terminal_transaction_start')
    payment_info = request.json['params']['payment_info']
    app.logger.debug('Telium: payment_info=%s', payment_info)
    telium_driver.push_task('transaction_start', payment_info)
    return jsonify(jsonrpc='2.0', result=True)


@app.route('/telium_status.html', methods=['POST'])
@cross_origin()
def telium_status():
    info = telium_driver.get_payment_info_from_price(
        float(request.values['price']),
        request.values['payment_mode'])
    app.logger.debug('Telium status info=%s', info)
    telium_driver.push_task('transaction_start', json.dumps(
        info, sort_keys=True))
    return render_template('telium_status.html')

