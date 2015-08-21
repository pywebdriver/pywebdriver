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

from pywebdriver import app, drivers
from flask_cors import cross_origin
from flask import request, jsonify
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

    def get_status(self):
        self.status = {'status': 'connected', 'messages': []}

        telium_driver.push_task('transaction_start', json.dumps({
            'amount': 999.99,
            'payment_mode': 'card',
            'currency_iso': 'EUR',
        }, sort_keys=True))
        if self.status['status'] == 'connected':
            # TODO Improve : Get the real modele connected
            self.vendor_product = 'telium_image'
        else:
            self.vendor_product = False
        return self.status

telium_driver = TeliumDriver(app.config)
drivers['telium'] = telium_driver

@app.route(
    '/hw_proxy/payment_terminal_transaction_start',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def payment_terminal_transaction_start(self, payment_info):
    app.logger.debug('Telium: Call payment_terminal_transaction_start')
    telium_driver.push_task('transaction_start', payment_info)
    return jsonify(jsonrpc='2.0', result=True)
