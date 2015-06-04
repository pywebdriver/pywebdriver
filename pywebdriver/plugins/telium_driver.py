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

meta = {
    'name': "POS Telium payment terminal",
    'description': """This plugin add the support of Telium payment terminal
        pywebdriver""",
    'require_pip': ['pypostelium'],
    'require_debian': ['python-pypostelium'],
}

from pywebdriver import app
from flask_cors import cross_origin
from flask import request, jsonify
from base_driver import ThreadDriver, check
import simplejson

try:
    import pypostelium
except:
    installed = False
else:
    installed = True

    class TeliumDriver(ThreadDriver, pypostelium.Driver):
        """ Telium Driver class for pywebdriver """

    telium_driver = TeliumDriver(app.config)

@app.route(
    '/hw_proxy/payment_terminal_transaction_start',
    methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@check(installed, meta)
def payment_terminal_transaction_start(self, payment_info):
    app.logger.debug('Telium: Call payment_terminal_transaction_start')
    telium_driver.push_task('transaction_start', payment_info)
    return jsonify(jsonrpc='2.0', result=True)
